#!/usr/bin/env python3
"""
Sync All Content from ERPNext

This script fetches all website content from ERPNext and generates
Hugo-compatible markdown files and data files.

Content Types Synced:
- Training courses and schedules
- Blog articles (with images)
- Portfolio items (with images)
- Team members
- Any other content stored in ERPNext

Features:
- Modular sync system for different content types
- Image downloading and caching
- Smart caching to avoid excessive API calls
- Configurable cache TTL per content type
- Error handling and fallback to cached data
- ERPNext API authentication

Usage:
    ./scripts/sync-content-from-erpnext.py [options]

Options:
    --force              Force refresh all content (ignore cache)
    --cache-ttl HOURS    Default cache TTL in hours (default: 6)
    --dry-run            Fetch data but don't write files
    --only TYPE          Only sync specific content type (training, blog, portfolio, etc.)
    --skip-images        Don't download images

Environment Variables:
    ERPNEXT_API_URL      - Base URL of your ERPNext instance
    ERPNEXT_API_KEY      - API key for authentication
    ERPNEXT_API_SECRET   - API secret for authentication
"""

import os
import sys
import json
import yaml
import requests
import argparse
import hashlib
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
import re


# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / ".cache"
IMAGES_CACHE_DIR = CACHE_DIR / "images"
CONTENT_DIR = PROJECT_ROOT / "content"
STATIC_DIR = PROJECT_ROOT / "static"
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_CACHE_TTL_HOURS = 6

# Cache files for different content types
CACHE_FILES = {
    'training': CACHE_DIR / 'training_cache.json',
    'blog': CACHE_DIR / 'blog_cache.json',
    'portfolio': CACHE_DIR / 'portfolio_cache.json',
    'team': CACHE_DIR / 'team_cache.json',
}


class ERPNextContentSync:
    """Sync all content from ERPNext to Hugo"""

    def __init__(self, api_url: str, api_key: str, api_secret: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {api_key}:{api_secret}',
            'Content-Type': 'application/json'
        })
        self.images_downloaded = {}

    # ============================================
    # TRAINING CONTENT SYNC
    # ============================================

    def sync_training_content(self) -> Dict:
        """Sync training courses, sessions, and pricing"""
        print("→ Syncing training content...")

        courses = self.fetch_training_courses()
        print(f"  ✓ Fetched {len(courses)} courses")

        sessions = self.fetch_training_sessions()
        print(f"  ✓ Fetched {len(sessions)} sessions")

        pricing = self.fetch_training_pricing()
        print(f"  ✓ Fetched {len(pricing)} pricing entries")

        return self.transform_training_data(courses, sessions, pricing)

    def fetch_training_courses(self) -> List[Dict]:
        """Fetch all training courses from ERPNext"""
        try:
            response = self.session.get(
                f"{self.api_url}/api/resource/Item",
                params={
                    'filters': json.dumps([
                        ["item_group", "=", "Training Courses"],
                        ["disabled", "=", 0]
                    ]),
                    'fields': json.dumps([
                        "name", "item_code", "item_name", "description",
                        "standard_rate", "item_group"
                    ])
                }
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"  ✗ Error fetching courses: {e}", file=sys.stderr)
            return []

    def fetch_training_sessions(self) -> List[Dict]:
        """Fetch scheduled training sessions from ERPNext"""
        try:
            response = self.session.get(
                f"{self.api_url}/api/resource/Event",
                params={
                    'filters': json.dumps([
                        ["event_category", "=", "Training"],
                        ["starts_on", ">=", datetime.now().isoformat()],
                        ["event_type", "=", "Public"]
                    ]),
                    'fields': json.dumps([
                        "name", "subject", "starts_on", "ends_on",
                        "description", "event_participants"
                    ]),
                    'limit_page_length': 100
                }
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"  ✗ Error fetching sessions: {e}", file=sys.stderr)
            return []

    def fetch_training_pricing(self) -> Dict:
        """Fetch pricing information from ERPNext"""
        try:
            response = self.session.get(
                f"{self.api_url}/api/resource/Item Price",
                params={
                    'filters': json.dumps([
                        ["item_group", "=", "Training Courses"]
                    ]),
                    'fields': json.dumps([
                        "item_code", "price_list", "price_list_rate", "currency"
                    ]),
                    'limit_page_length': 500
                }
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"  ✗ Error fetching pricing: {e}", file=sys.stderr)
            return []

    def transform_training_data(self, courses: List[Dict], sessions: List[Dict],
                                pricing: List[Dict]) -> Dict:
        """Transform ERPNext training data to Hugo format"""

        venues = {
            "cape-town": {
                "name": "Cape Town, South Africa",
                "address": "Kartoza Office, Black River Park, Observatory, Cape Town",
                "type": "in-person",
                "icon": "fa-building",
                "description": "Our headquarters with fully-equipped training facilities"
            },
            "johannesburg": {
                "name": "Johannesburg, South Africa",
                "address": "Sandton Convention Centre",
                "type": "in-person",
                "icon": "fa-building",
                "description": "Central location in Johannesburg's business district"
            },
            "remote": {
                "name": "Online / Remote",
                "address": "Live virtual classroom",
                "type": "remote",
                "icon": "fa-video",
                "description": "Join from anywhere with our interactive online sessions"
            },
            "on-site": {
                "name": "Your Location",
                "address": "We come to you",
                "type": "on-site",
                "icon": "fa-map-marker-alt",
                "description": "Custom training at your office or preferred venue"
            }
        }

        currencies = {
            "ZAR": {"symbol": "R", "name": "South African Rand", "code": "ZAR"},
            "USD": {"symbol": "$", "name": "US Dollar", "code": "USD"},
            "EUR": {"symbol": "€", "name": "Euro", "code": "EUR"}
        }

        # Transform pricing
        pricing_dict = {}
        for price in pricing:
            item_code = price.get('item_code', '').lower().replace(' ', '-')
            currency = price.get('currency', 'ZAR')
            rate = price.get('price_list_rate', 0)

            if item_code not in pricing_dict:
                pricing_dict[item_code] = {}
            if currency not in pricing_dict[item_code]:
                pricing_dict[item_code][currency] = {}

            pricing_dict[item_code][currency]['in-person'] = rate
            pricing_dict[item_code][currency]['remote'] = rate * 0.75
            pricing_dict[item_code][currency]['on-site'] = None

        # Transform sessions
        sessions_list = []
        for session in sessions:
            sessions_list.append({
                'id': session.get('name', ''),
                'course': self._extract_course_slug(session.get('subject', '')),
                'venue': self._determine_venue(session),
                'start_date': session.get('starts_on', '').split('T')[0] if session.get('starts_on') else '',
                'end_date': session.get('ends_on', '').split('T')[0] if session.get('ends_on') else '',
                'seats_total': 15,
                'seats_available': 10,
                'instructor': self._extract_instructor(session),
                'status': 'open'
            })

        return {
            'venues': venues,
            'currencies': currencies,
            'pricing': pricing_dict,
            'sessions': sessions_list,
            'group_discounts': [
                {'min_attendees': 3, 'max_attendees': 5, 'discount_percent': 10, 'label': 'Small Team'},
                {'min_attendees': 6, 'max_attendees': 10, 'discount_percent': 15, 'label': 'Team'},
                {'min_attendees': 11, 'max_attendees': 20, 'discount_percent': 20, 'label': 'Large Team'},
                {'min_attendees': 21, 'max_attendees': None, 'discount_percent': 25, 'label': 'Enterprise'}
            ],
            'early_bird': {'days_before': 30, 'discount_percent': 10},
            'api': {
                'base_url': f"{self.api_url}/api/v1",
                'endpoints': {
                    'check_availability': '/training/sessions/{session_id}/availability',
                    'create_booking': '/training/bookings',
                    'get_pricing': '/training/pricing/{course_slug}'
                }
            }
        }

    # ============================================
    # BLOG CONTENT SYNC
    # ============================================

    def sync_blog_content(self, download_images: bool = True) -> dict:
        """Sync blog articles by calling fetch-erpnext-blogs.py"""
        print("→ Syncing blog articles...")

        # Build command
        cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "fetch-erpnext-blogs.py")]
        if not download_images:
            cmd.append("--skip-images")

        # Run and capture output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=os.environ,
            cwd=PROJECT_ROOT
        )

        # Print stderr (the status table) to console
        if result.stderr:
            print(result.stderr)

        # Parse JSON summary from stdout
        if result.stdout.strip():
            try:
                summary = json.loads(result.stdout.strip().split('\n')[-1])
                print(f"  ✓ Processed {summary['total']} articles: {summary['new']} new, {summary['unchanged']} unchanged, {summary['updated']} updated")
                return summary
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                print(f"  ✗ Error parsing sync output: {e}", file=sys.stderr)

        return {'total': 0, 'new': 0, 'unchanged': 0, 'updated': 0, 'errors': 0}

    def fetch_blog_articles(self) -> List[Dict]:
        """Fetch blog articles from ERPNext"""
        try:
            # Adjust based on your ERPNext blog structure
            # Could be: Blog Post, Custom DocType, etc.
            response = self.session.get(
                f"{self.api_url}/api/resource/Blog Post",
                params={
                    'filters': json.dumps([
                        ["published", "=", 1]
                    ]),
                    'fields': json.dumps([
                        "name", "title", "blog_intro", "content",
                        "published_on", "blogger", "meta_title",
                        "meta_description", "route", "featured_image",
                        "tags"
                    ]),
                    'limit_page_length': 500
                }
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"  ✗ Error fetching blog articles: {e}", file=sys.stderr)
            return []

    def transform_blog_article(self, article: Dict, download_images: bool) -> Optional[Dict]:
        """Transform ERPNext blog article to Hugo format"""
        try:
            slug = article.get('route', '').replace('/blog/', '').strip('/')
            if not slug:
                slug = self._slugify(article.get('title', ''))

            # Download featured image if exists
            featured_image = None
            if download_images and article.get('featured_image'):
                featured_image = self.download_image(
                    article['featured_image'],
                    f"blog/{slug}"
                )

            # Process content images
            content = article.get('content', '')
            if download_images:
                content = self.process_content_images(content, f"blog/{slug}")

            # Extract and process tags
            tags = []
            if article.get('tags'):
                tags = [tag.strip() for tag in article.get('tags', '').split(',')]

            return {
                'slug': slug,
                'title': article.get('title', ''),
                'description': article.get('blog_intro', ''),
                'content': content,
                'date': article.get('published_on', datetime.now().isoformat()),
                'author': article.get('blogger', 'Kartoza'),
                'featured_image': featured_image,
                'tags': tags,
                'meta_title': article.get('meta_title', article.get('title', '')),
                'meta_description': article.get('meta_description', article.get('blog_intro', ''))
            }
        except Exception as e:
            print(f"  ✗ Error transforming article {article.get('title')}: {e}", file=sys.stderr)
            return None

    def write_blog_article(self, article: Dict):
        """Write blog article as Hugo markdown file"""
        blog_dir = CONTENT_DIR / "blog"
        blog_dir.mkdir(parents=True, exist_ok=True)

        filename = blog_dir / f"{article['slug']}.md"

        # Build frontmatter
        frontmatter = {
            'title': article['title'],
            'description': article['description'],
            'date': article['date'],
            'author': article['author'],
            'tags': article['tags']
        }

        if article.get('featured_image'):
            frontmatter['featured_image'] = article['featured_image']

        if article.get('meta_title'):
            frontmatter['meta_title'] = article['meta_title']

        if article.get('meta_description'):
            frontmatter['meta_description'] = article['meta_description']

        # Write file
        with open(filename, 'w') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
            f.write('---\n\n')
            f.write(article['content'])

    # ============================================
    # PORTFOLIO CONTENT SYNC
    # ============================================

    def sync_portfolio_content(self, download_images: bool = True) -> List[Dict]:
        """Sync portfolio items from ERPNext"""
        print("→ Syncing portfolio items...")

        items = self.fetch_portfolio_items()
        print(f"  ✓ Fetched {len(items)} portfolio items")

        processed_items = []
        for item in items:
            processed = self.transform_portfolio_item(item, download_images)
            if processed:
                processed_items.append(processed)
                self.write_portfolio_item(processed)

        print(f"  ✓ Processed {len(processed_items)} portfolio items")
        return processed_items

    def fetch_portfolio_items(self) -> List[Dict]:
        """Fetch portfolio items from ERPNext"""
        try:
            # Adjust based on your ERPNext portfolio structure
            response = self.session.get(
                f"{self.api_url}/api/resource/Project",
                params={
                    'filters': json.dumps([
                        ["is_published", "=", 1],
                        ["project_type", "=", "Portfolio"]
                    ]),
                    'fields': json.dumps([
                        "name", "project_name", "description",
                        "project_image", "client", "start_date",
                        "end_date", "status", "tags"
                    ]),
                    'limit_page_length': 500
                }
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"  ✗ Error fetching portfolio items: {e}", file=sys.stderr)
            return []

    def transform_portfolio_item(self, item: Dict, download_images: bool) -> Optional[Dict]:
        """Transform ERPNext portfolio item to Hugo format"""
        try:
            slug = self._slugify(item.get('project_name', ''))

            # Download project image
            project_image = None
            if download_images and item.get('project_image'):
                project_image = self.download_image(
                    item['project_image'],
                    f"portfolio/{slug}"
                )

            # Extract tags
            tags = []
            if item.get('tags'):
                tags = [tag.strip() for tag in item.get('tags', '').split(',')]

            return {
                'slug': slug,
                'title': item.get('project_name', ''),
                'description': item.get('description', ''),
                'client': item.get('client', ''),
                'start_date': item.get('start_date', ''),
                'end_date': item.get('end_date', ''),
                'status': item.get('status', ''),
                'image': project_image,
                'tags': tags
            }
        except Exception as e:
            print(f"  ✗ Error transforming portfolio item {item.get('project_name')}: {e}", file=sys.stderr)
            return None

    def write_portfolio_item(self, item: Dict):
        """Write portfolio item as Hugo markdown file"""
        portfolio_dir = CONTENT_DIR / "portfolio"
        portfolio_dir.mkdir(parents=True, exist_ok=True)

        filename = portfolio_dir / f"{item['slug']}.md"

        # Build frontmatter
        frontmatter = {
            'title': item['title'],
            'description': item['description'],
            'client': item['client'],
            'start_date': item['start_date'],
            'end_date': item['end_date'],
            'status': item['status'],
            'tags': item['tags']
        }

        if item.get('image'):
            frontmatter['image'] = item['image']

        # Write file
        with open(filename, 'w') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True)
            f.write('---\n\n')
            f.write(item['description'])

    # ============================================
    # IMAGE DOWNLOADING AND CACHING
    # ============================================

    def download_image(self, image_url: str, context: str) -> Optional[str]:
        """Download and cache an image from ERPNext"""
        try:
            # Handle relative URLs
            if not image_url.startswith('http'):
                image_url = urljoin(self.api_url, image_url)

            # Generate unique filename based on URL
            url_hash = hashlib.md5(image_url.encode()).hexdigest()[:8]
            parsed = urlparse(image_url)
            ext = Path(parsed.path).suffix or '.jpg'
            filename = f"{context.replace('/', '-')}-{url_hash}{ext}"

            # Cache path
            cache_path = IMAGES_CACHE_DIR / filename

            # Check if already downloaded
            if cache_path.exists():
                print(f"    ✓ Using cached image: {filename}")
                relative_path = f"/img/synced/{filename}"
                self.images_downloaded[image_url] = relative_path
                return relative_path

            # Download image
            print(f"    ↓ Downloading: {filename}")
            response = self.session.get(image_url, timeout=30)
            response.raise_for_status()

            # Save to cache
            IMAGES_CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_path.write_bytes(response.content)

            # Copy to static directory
            static_img_dir = STATIC_DIR / "img" / "synced"
            static_img_dir.mkdir(parents=True, exist_ok=True)
            static_path = static_img_dir / filename
            static_path.write_bytes(response.content)

            relative_path = f"/img/synced/{filename}"
            self.images_downloaded[image_url] = relative_path
            print(f"    ✓ Downloaded: {filename}")
            return relative_path

        except Exception as e:
            print(f"    ✗ Error downloading {image_url}: {e}", file=sys.stderr)
            return None

    def process_content_images(self, content: str, context: str) -> str:
        """Find and download all images in HTML content"""
        # Find all image URLs in content
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        matches = re.findall(img_pattern, content)

        for img_url in matches:
            local_path = self.download_image(img_url, context)
            if local_path:
                content = content.replace(img_url, local_path)

        return content

    # ============================================
    # UTILITY METHODS
    # ============================================

    def _slugify(self, text: str) -> str:
        """Convert text to URL-friendly slug"""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text)
        text = re.sub(r'^-+|-+$', '', text)
        return text

    def _extract_course_slug(self, subject: str) -> str:
        """Extract course slug from session subject"""
        course_map = {
            'qgis introduction': 'qgis-introduction',
            'advanced qgis': 'qgis-advanced',
            'postgis': 'postgis',
            'geoserver': 'geoserver',
            'geonode': 'geonode',
            'python for gis': 'python-gis',
            'web mapping': 'web-mapping',
            'open data': 'open-data'
        }

        subject_lower = subject.lower()
        for key, slug in course_map.items():
            if key in subject_lower:
                return slug
        return 'unknown'

    def _determine_venue(self, session: Dict) -> str:
        """Determine venue from session data"""
        description = session.get('description', '').lower()
        if 'remote' in description or 'online' in description:
            return 'remote'
        elif 'johannesburg' in description:
            return 'johannesburg'
        elif 'on-site' in description or 'client site' in description:
            return 'on-site'
        else:
            return 'cape-town'

    def _extract_instructor(self, session: Dict) -> str:
        """Extract instructor name from session"""
        participants = session.get('event_participants', [])
        if participants and len(participants) > 0:
            return participants[0].get('reference_docname', 'TBA')
        return 'TBA'


# ============================================
# CACHING FUNCTIONS
# ============================================

def load_cache(cache_file: Path, ttl_hours: int) -> Optional[Dict]:
    """Load cached data if still valid"""
    if not cache_file.exists():
        return None

    try:
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)

        cached_time = datetime.fromisoformat(cache_data['timestamp'])
        age = datetime.now() - cached_time

        if age < timedelta(hours=ttl_hours):
            print(f"✓ Using cached data (age: {age.total_seconds() / 3600:.1f} hours)")
            return cache_data['data']
        else:
            print(f"✗ Cache expired (age: {age.total_seconds() / 3600:.1f} hours)")
            return None
    except Exception as e:
        print(f"✗ Error loading cache: {e}")
        return None


def save_cache(cache_file: Path, data: Dict):
    """Save data to cache"""
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_data = {
        'timestamp': datetime.now().isoformat(),
        'data': data
    }
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f, indent=2)
    print(f"✓ Cache saved to {cache_file.name}")


def save_yaml(output_file: Path, data: Dict):
    """Save data to YAML file"""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        f.write("# Training Schedule and Pricing Data\n")
        f.write("# This file is auto-generated from ERPNext\n")
        f.write(f"# Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("# DO NOT EDIT MANUALLY - Changes will be overwritten\n\n")
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    print(f"✓ Saved to {output_file.relative_to(PROJECT_ROOT)}")


# ============================================
# MAIN
# ============================================

def main():
    parser = argparse.ArgumentParser(description='Sync all content from ERPNext')
    parser.add_argument('--force', action='store_true',
                        help='Force refresh, ignore cache')
    parser.add_argument('--cache-ttl', type=int, default=DEFAULT_CACHE_TTL_HOURS,
                        help=f'Cache TTL in hours (default: {DEFAULT_CACHE_TTL_HOURS})')
    parser.add_argument('--dry-run', action='store_true',
                        help='Fetch data but do not write files')
    parser.add_argument('--only', type=str, choices=['training', 'blog', 'portfolio', 'all'],
                        default='all', help='Only sync specific content type')
    parser.add_argument('--skip-images', action='store_true',
                        help='Skip downloading images')
    args = parser.parse_args()

    print("=" * 60)
    print("  Kartoza Content Sync from ERPNext")
    print("=" * 60)
    print()

    # Check for required environment variables
    api_url = os.getenv('ERPNEXT_API_URL')
    api_key = os.getenv('ERPNEXT_API_KEY')
    api_secret = os.getenv('ERPNEXT_API_SECRET')

    if not all([api_url, api_key, api_secret]):
        print("⚠ ERPNext credentials not found in environment variables", file=sys.stderr)
        print("  Using cached data or falling back to manual content", file=sys.stderr)
        print()

        # Try to use cache for all content types
        success = False
        if args.only in ['training', 'all']:
            cached = load_cache(CACHE_FILES['training'], args.cache_ttl)
            if cached and not args.dry_run:
                save_yaml(DATA_DIR / "training_schedule.yml", cached)
                success = True

        if not success:
            print("✗ No cache available and no credentials provided", file=sys.stderr)
            print("  Keeping existing content", file=sys.stderr)
            return 1

        return 0

    # Sync from ERPNext
    sync = ERPNextContentSync(api_url, api_key, api_secret)

    try:
        # Sync Training Content
        if args.only in ['training', 'all']:
            print()
            if not args.force:
                cached = load_cache(CACHE_FILES['training'], args.cache_ttl)
                if cached:
                    if not args.dry_run:
                        save_yaml(DATA_DIR / "training_schedule.yml", cached)
                else:
                    training_data = sync.sync_training_content()
                    save_cache(CACHE_FILES['training'], training_data)
                    if not args.dry_run:
                        save_yaml(DATA_DIR / "training_schedule.yml", training_data)
            else:
                training_data = sync.sync_training_content()
                save_cache(CACHE_FILES['training'], training_data)
                if not args.dry_run:
                    save_yaml(DATA_DIR / "training_schedule.yml", training_data)

        # Sync Blog Content
        if args.only in ['blog', 'all']:
            print()
            if not args.force:
                cached = load_cache(CACHE_FILES['blog'], args.cache_ttl)
                if cached:
                    print("✓ Using cached blog data")
                else:
                    blog_data = sync.sync_blog_content(download_images=not args.skip_images)
                    save_cache(CACHE_FILES['blog'], blog_data)
            else:
                blog_data = sync.sync_blog_content(download_images=not args.skip_images)
                save_cache(CACHE_FILES['blog'], blog_data)

        # Sync Portfolio Content
        if args.only in ['portfolio', 'all']:
            print()
            if not args.force:
                cached = load_cache(CACHE_FILES['portfolio'], args.cache_ttl)
                if cached:
                    print("✓ Using cached portfolio data")
                else:
                    portfolio_data = sync.sync_portfolio_content(download_images=not args.skip_images)
                    save_cache(CACHE_FILES['portfolio'], portfolio_data)
            else:
                portfolio_data = sync.sync_portfolio_content(download_images=not args.skip_images)
                save_cache(CACHE_FILES['portfolio'], portfolio_data)

        print()
        print("=" * 60)
        print("  ✓ Content sync completed successfully")
        print("=" * 60)
        return 0

    except Exception as e:
        print()
        print(f"✗ Error syncing from ERPNext: {e}", file=sys.stderr)

        # Fallback to cache on error
        print("→ Attempting fallback to cached data...", file=sys.stderr)
        fallback_success = False

        if args.only in ['training', 'all']:
            cached = load_cache(CACHE_FILES['training'], 999999)
            if cached and not args.dry_run:
                save_yaml(DATA_DIR / "training_schedule.yml", cached)
                fallback_success = True

        if fallback_success:
            print("→ Using cached data as fallback", file=sys.stderr)
            return 0
        else:
            print("✗ No fallback cache available", file=sys.stderr)
            return 1


if __name__ == '__main__':
    sys.exit(main())
