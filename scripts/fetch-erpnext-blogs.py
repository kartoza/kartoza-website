#!/usr/bin/env python3
"""
Sync blog articles from ERPNext to Hugo with fidelity checking.

Features:
- Fetches all published blog articles from ERPNext
- Compares with local Hugo content (text-only, ignoring formatting)
- ERPNext is authoritative: overwrites local content when different
- Auto-marks articles as reviewed when fidelity check passes
- Outputs rich status table and JSON summary

Environment variables:
    ERPNEXT_URL: ERPNext instance URL (default: https://erp.kartoza.com)

Usage:
    ./fetch-erpnext-blogs.py              # Full sync with fidelity checking
    ./fetch-erpnext-blogs.py --dry-run    # Preview changes without writing
    ./fetch-erpnext-blogs.py --list       # List available blogs
    ./fetch-erpnext-blogs.py --verbose    # Verbose output
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

import warnings

import requests
import yaml
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from dateutil import parser as date_parser
from tabulate import tabulate
import json
import html2text

# Suppress XML parsing warning when using html.parser on content that looks like XML
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


# Configuration
ERPNEXT_URL = os.environ.get('ERPNEXT_URL', 'https://erp.kartoza.com')
KARTOZA_URL = 'https://kartoza.com'

# Image storage path relative to Hugo static folder
IMAGE_DIR = 'img/blog/erpnext'


def get_auth_headers() -> dict:
    """Get authentication headers for ERPNext API (empty for public blogs)."""
    return {}


def download_image(url: str, static_dir: Path, verbose: bool = False) -> str | None:
    """
    Download an image from ERPNext and save it locally.

    Args:
        url: The image URL (can be relative like /files/xxx or absolute)
        static_dir: Path to Hugo's static directory

    Returns:
        Local path to use in markdown (e.g., /img/blog/erpnext/xxx.png) or None on failure
    """
    # Normalize the URL
    if url.startswith('/files/'):
        full_url = f"{KARTOZA_URL}{url}"
        filename = url.split('/')[-1]
    elif url.startswith('/'):
        full_url = f"{KARTOZA_URL}{url}"
        filename = url.split('/')[-1]
    elif 'kartoza.com/files/' in url or 'erp.kartoza.com/files/' in url:
        full_url = url
        filename = url.split('/')[-1]
    else:
        # Not a Kartoza image, leave as-is
        return None

    # Create target directory
    target_dir = static_dir / IMAGE_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / filename
    local_url = f"/{IMAGE_DIR}/{filename}"

    # Skip if already downloaded
    if target_path.exists():
        return local_url

    # Download the image
    try:
        if verbose:
            print(f"  Downloading: {filename}", file=sys.stderr)
        response = requests.get(full_url, timeout=30)
        response.raise_for_status()
        target_path.write_bytes(response.content)
        return local_url
    except requests.RequestException as e:
        print(f"  Warning: Failed to download {full_url}: {e}", file=sys.stderr)
        return None


def process_images_in_content(content: str, static_dir: Path, verbose: bool = False) -> str:
    """
    Find all images in markdown content, download them, and rewrite URLs.

    Args:
        content: Markdown content with image references
        static_dir: Path to Hugo's static directory

    Returns:
        Content with rewritten image URLs
    """
    # Pattern for markdown images: ![alt](/files/xxx) or ![alt](https://kartoza.com/files/xxx)
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    def replace_image(match):
        alt_text = match.group(1)
        img_url = match.group(2)

        # Try to download and get local path
        local_path = download_image(img_url, static_dir, verbose=verbose)

        if local_path:
            return f'![{alt_text}]({local_path})'
        else:
            # Keep original URL if download failed or not a Kartoza image
            return match.group(0)

    return img_pattern.sub(replace_image, content)


def process_thumbnail(thumbnail_url: str, static_dir: Path, verbose: bool = False) -> str:
    """
    Download thumbnail image and return local path.

    Args:
        thumbnail_url: The thumbnail URL
        static_dir: Path to Hugo's static directory

    Returns:
        Local path or original URL if download failed
    """
    if not thumbnail_url:
        return '/img/blog/placeholder.png'

    local_path = download_image(thumbnail_url, static_dir, verbose=verbose)
    return local_path if local_path else thumbnail_url


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def normalize_for_comparison(content: str) -> str:
    """
    Normalize content for fidelity comparison.
    Focuses on TEXT content, ignores formatting/layout.
    """
    if not content:
        return ''

    # Remove Hugo shortcodes like {{< block >}} or {{< /block >}}
    content = re.sub(r'\{\{[<>%].*?[>%]\}\}', '', content)

    # Strip HTML tags but keep text content
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text(separator=' ')

    # Collapse whitespace (multiple spaces/newlines -> single space)
    text = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing whitespace and lowercase
    return text.strip().lower()


def check_fidelity(local_content: str, erpnext_content: str) -> bool:
    """
    Check if local and ERPNext content match (fidelity check).

    Returns True if text content matches (ignoring formatting).
    """
    local_norm = normalize_for_comparison(local_content)
    erpnext_norm = normalize_for_comparison(erpnext_content)
    return local_norm == erpnext_norm


def read_local_blog(filepath: Path) -> tuple[dict, str] | None:
    """
    Read a local Hugo blog file and extract front matter and content.

    Returns:
        Tuple of (front_matter_dict, content_str) or None if file doesn't exist
    """
    if not filepath.exists():
        return None

    try:
        text = filepath.read_text()
    except (IOError, OSError):
        return None

    # Check for front matter delimiter
    if not text.startswith('---'):
        return {}, text

    # Find end of front matter
    end_match = re.search(r'\n---\n', text[3:])
    if not end_match:
        return {}, text

    end_pos = end_match.start() + 3
    front_matter_raw = text[4:end_pos]
    content = text[end_pos + 5:]

    try:
        front_matter = yaml.safe_load(front_matter_raw) or {}
    except yaml.YAMLError:
        front_matter = {}

    return front_matter, content


def find_local_file(content_dir: Path, erpnext_id: str, title: str) -> Path | None:
    """
    Find a local Hugo file matching the ERPNext article.

    Matches by:
    1. erpnext_id in front matter (primary)
    2. Slugified title matching filename (fallback)

    Returns:
        Path to matching file or None
    """
    # First, try to find by erpnext_id in front matter
    for filepath in content_dir.glob('*.md'):
        if filepath.name == '_index.md':
            continue
        result = read_local_blog(filepath)
        if result:
            front_matter, _ = result
            if front_matter.get('erpnext_id') == erpnext_id:
                return filepath

    # Fallback: match by slugified title
    expected_filename = f"{slugify(title)}.md"
    expected_path = content_dir / expected_filename
    if expected_path.exists():
        return expected_path

    return None


def sync_blog(blog: dict, content_dir: Path, static_dir: Path, dry_run: bool = False,
               force: bool = False, skip_images: bool = False, verbose: bool = False) -> dict:
    """
    Sync a single blog article from ERPNext to Hugo.

    Performs fidelity checking and updates review fields.

    Args:
        blog: Blog data from ERPNext
        content_dir: Path to Hugo content directory
        static_dir: Path to Hugo static directory (for images)
        dry_run: If True, don't write files
        force: If True, overwrite all files regardless of fidelity
        skip_images: If True, don't download images
        verbose: If True, show detailed output

    Returns:
        Dict with 'status' and 'fidelity' keys
    """
    erpnext_id = blog.get('name', '')
    title = blog.get('title', 'Untitled')
    erpnext_content = blog.get('content') or blog.get('content_html') or ''

    # Find existing local file
    local_file = find_local_file(content_dir, erpnext_id, title)

    if local_file and not force:
        # File exists - check fidelity (skip if force mode)
        result = read_local_blog(local_file)
        if result:
            local_frontmatter, local_content = result
            if check_fidelity(local_content, erpnext_content):
                # Content matches - fidelity passed
                # Update review fields if not already set
                if not local_frontmatter.get('reviewedBy'):
                    if not dry_run:
                        _update_review_fields(local_file, local_frontmatter, local_content)
                return {'status': 'unchanged', 'fidelity': 'passed', 'file': local_file.name}

        # Content differs - overwrite with ERPNext
        status = 'updated'
        filepath = local_file
    elif local_file and force:
        # Force mode - overwrite existing file
        status = 'forced'
        filepath = local_file
    else:
        # New file
        status = 'new'
        slug = slugify(title)
        filepath = content_dir / f"{slug}.md"

    # Generate content
    front_matter = blog_to_hugo_frontmatter(blog, mark_reviewed=True)
    content = blog_to_hugo_content(blog)

    # Process images (download and rewrite URLs)
    if not skip_images and not dry_run:
        content = process_images_in_content(content, static_dir, verbose=verbose)
        # Also process thumbnail
        if front_matter.get('thumbnail'):
            front_matter['thumbnail'] = process_thumbnail(
                front_matter['thumbnail'], static_dir, verbose=verbose
            )

    # Build file content
    file_content = "---\n"
    file_content += yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
    file_content += "---\n\n"
    file_content += content
    file_content += "\n"

    if not dry_run:
        filepath.write_text(file_content)

    return {'status': status, 'fidelity': 'auto-reviewed', 'file': filepath.name}


def _update_review_fields(filepath: Path, front_matter: dict, content: str) -> None:
    """Update review fields in an existing file."""
    front_matter['reviewedBy'] = 'Automated Check'
    front_matter['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')

    file_content = "---\n"
    file_content += yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
    file_content += "---\n\n"
    file_content += content.strip()
    file_content += "\n"

    filepath.write_text(file_content)


def fetch_blog_list() -> list[dict]:
    """Fetch list of all published blog posts using the public list API with pagination."""
    blogs = []
    limit_start = 0
    page_size = 20

    while True:
        url = f"{ERPNEXT_URL}/api/method/frappe.www.list.get"
        params = {
            'doctype': 'Blog Post',
            'limit_start': limit_start,
            'pathname': '/blog'
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching blog list (page {limit_start // page_size + 1}): {e}", file=sys.stderr)
            break
        except json.JSONDecodeError as e:
            print(f"Error parsing blog list response: {e}", file=sys.stderr)
            break

        message = data.get('message', {})
        raw_result = message.get('raw_result', '[]')

        # Parse the raw_result JSON string
        try:
            page_blogs = json.loads(raw_result) if isinstance(raw_result, str) else raw_result
        except json.JSONDecodeError:
            page_blogs = []

        if not page_blogs:
            break

        # Transform to our format
        for blog in page_blogs:
            route = blog.get('route', '')
            blogs.append({
                'name': f"/{route}" if route and not route.startswith('/') else route,
                'title': blog.get('title', 'Untitled'),
                'blog_category': blog.get('blog_category', 'uncategorised'),
                'published_on': blog.get('published_on', ''),
                'blogger': blog.get('blogger', 'Kartoza'),
                'content': blog.get('content', ''),
                'cover_image': blog.get('cover_image', ''),
                'modified': blog.get('published_on', ''),  # Use published date as modified
            })

        # Check if there are more pages
        show_more = message.get('show_more', False)
        next_start = message.get('next_start', 0)

        if not show_more or next_start <= limit_start:
            break

        limit_start = next_start

    return blogs


def fetch_blog_detail(name: str) -> dict | None:
    """
    Fetch full blog post details.

    Since fetch_blog_list now returns full details, this function just returns
    the blog data if it was passed directly, or fetches from the web page as fallback.
    """
    # If name is already a dict with full data, return it
    if isinstance(name, dict):
        return name

    # Fallback: scrape the public blog page
    url = f"{ERPNEXT_URL}{name}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching blog '{name}': {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract metadata from meta tags
    def get_meta(attr_name, attr_value):
        tag = soup.find('meta', attrs={attr_name: attr_value})
        return tag.get('content', '') if tag else ''

    # Get title from og:title (has proper capitalization) or meta name
    title = get_meta('property', 'og:title') or get_meta('name', 'title') or get_meta('name', 'name')
    if not title:
        h1 = soup.find('h1', class_='blog-title')
        title = h1.get_text(strip=True) if h1 else 'Untitled'
    # Clean up title prefix
    title = re.sub(r'^Kartoza\s*-\s*', '', title)

    # Get description/intro
    description = get_meta('name', 'description') or get_meta('property', 'og:description')
    if not description:
        intro = soup.find('p', class_='blog-intro')
        description = intro.get_text(strip=True) if intro else ''

    # Get author - prefer full name from avatar/author link over meta tag username
    author = None
    # Try to get full name from avatar span
    avatar_span = soup.find('span', class_='avatar', attrs={'title': True})
    if avatar_span:
        author = avatar_span.get('title')
    # Or from author link
    if not author:
        author_link = soup.find('a', href=lambda h: h and '/blog?blogger=' in h)
        if author_link:
            author = author_link.get_text(strip=True)
    # Fallback to meta tag
    if not author:
        author = get_meta('name', 'author') or get_meta('property', 'og:author') or 'Kartoza'

    # Get published date
    published_on = get_meta('name', 'datePublished') or get_meta('property', 'og:published_on')
    if not published_on:
        time_tag = soup.find('time', attrs={'datetime': True})
        published_on = time_tag['datetime'] if time_tag else ''

    # Get featured image
    image = get_meta('name', 'image') or get_meta('property', 'og:image') or ''

    # Get content from article body
    content = ''
    article_body = soup.find('div', attrs={'itemprop': 'articleBody'})
    if article_body:
        content = str(article_body)

    # Extract category from URL path
    parts = name.split('/')
    category = parts[2] if len(parts) >= 3 else 'uncategorised'

    return {
        'name': name,
        'title': title,
        'blog_intro': description,
        'blogger': author,
        'published_on': published_on,
        'modified': published_on,  # Use published date as modified
        'blog_category': category,
        'content': content,
        'featured_image': image,
    }


def blog_to_hugo_frontmatter(blog: dict, mark_reviewed: bool = False) -> dict:
    """Convert ERPNext blog to Hugo front matter."""
    # Parse date
    pub_date = blog.get('published_on') or blog.get('creation')
    if pub_date:
        try:
            dt = date_parser.parse(pub_date)
            date_str = dt.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            date_str = datetime.now().strftime('%Y-%m-%d')
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # Get thumbnail from featured_image or use placeholder
    # Get thumbnail from cover_image (API) or featured_image (scraping) or use placeholder
    thumbnail = blog.get('cover_image', '') or blog.get('featured_image', '') or '/img/blog/placeholder.png'
    # Ensure full URL for external images
    if thumbnail and not thumbnail.startswith(('http://', 'https://', '/')):
        thumbnail = f"{ERPNEXT_URL}/{thumbnail}"

    # Build front matter
    front_matter = {
        'title': blog.get('title', 'Untitled'),
        'description': blog.get('blog_intro', '')[:200] if blog.get('blog_intro') else '',
        'date': date_str,
        'author': blog.get('blogger', 'Kartoza'),
        'thumbnail': thumbnail,
        'tags': [],
        'erpnext_id': blog.get('name', ''),
        'erpnext_modified': blog.get('modified', ''),
    }

    # Add category as tag (capitalize first letter)
    if blog.get('blog_category'):
        category = blog['blog_category']
        # Capitalize first letter of each word
        category = category.replace('-', ' ').title()
        front_matter['tags'].append(category)

    # Add review fields if requested
    if mark_reviewed:
        front_matter['reviewedBy'] = 'Automated Check'
        front_matter['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')

    return front_matter


def blog_to_hugo_content(blog: dict) -> str:
    """Convert ERPNext blog content to Hugo markdown using html2text."""
    content = blog.get('content') or blog.get('content_html') or ''

    if not content:
        return ''

    # Configure html2text for clean markdown output
    h = html2text.HTML2Text()
    h.body_width = 0  # Don't wrap lines
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.skip_internal_links = False
    h.inline_links = True
    h.protect_links = True
    h.unicode_snob = True  # Use unicode instead of ASCII

    # Convert HTML to markdown
    markdown = h.handle(content)

    return markdown.strip()


def create_hugo_file(blog: dict, content_dir: Path, dry_run: bool = False) -> tuple[str, str]:
    """
    Create Hugo markdown file from ERPNext blog.

    Returns:
        Tuple of (filename, status)
    """
    title = blog.get('title', 'Untitled')
    slug = slugify(title)
    filename = f"{slug}.md"
    filepath = content_dir / filename

    # Check if file already exists
    if filepath.exists():
        return filename, 'Exists (skipped)'

    front_matter = blog_to_hugo_frontmatter(blog)
    content = blog_to_hugo_content(blog)

    # Build the file content
    file_content = "---\n"
    file_content += yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
    file_content += "---\n\n"
    file_content += content
    file_content += "\n"

    if not dry_run:
        filepath.write_text(file_content)
        return filename, 'Created'
    else:
        return filename, 'Would create'


def print_status_table(results: list[dict], dry_run: bool = False) -> None:
    """Print a rich status table of sync results to stderr."""
    if not results:
        print("\nNo blogs found.", file=sys.stderr)
        return

    # Prepare table data
    table_data = []
    for r in results:
        title = r['title'][:40] + ('...' if len(r['title']) > 40 else '')
        status = r['status']
        fidelity = r.get('fidelity', '-')

        # Format fidelity with symbols
        if fidelity == 'auto-reviewed':
            fidelity_str = '✓ auto-reviewed'
        elif fidelity == 'passed':
            fidelity_str = '✓ passed'
        elif fidelity == 'failed':
            fidelity_str = '✗ failed'
        else:
            fidelity_str = fidelity

        table_data.append([
            title,
            r.get('date', '-')[:10],
            r.get('author', '-')[:15],
            status,
            fidelity_str
        ])

    # Print header
    header = "ERPNEXT BLOG SYNC REPORT"
    if dry_run:
        header += " (DRY RUN)"

    print("\n" + "=" * 80, file=sys.stderr)
    print(f"  {header}", file=sys.stderr)
    print(f"  Source: {ERPNEXT_URL} | Date: {datetime.now().strftime('%Y-%m-%d')}", file=sys.stderr)
    print("=" * 80, file=sys.stderr)

    # Print table using tabulate
    headers = ['Title', 'Date', 'Author', 'Status', 'Fidelity']
    print(tabulate(table_data, headers=headers, tablefmt='simple'), file=sys.stderr)

    # Print summary
    print("-" * 80, file=sys.stderr)
    new_count = sum(1 for r in results if r['status'] == 'new')
    unchanged_count = sum(1 for r in results if r['status'] == 'unchanged')
    updated_count = sum(1 for r in results if r['status'] == 'updated')
    error_count = sum(1 for r in results if r['status'] == 'error')

    print(f"  Summary: {len(results)} total | {new_count} new | {unchanged_count} unchanged | {updated_count} updated | {error_count} errors", file=sys.stderr)
    print("=" * 80, file=sys.stderr)


def output_json_summary(results: list[dict]) -> None:
    """Output JSON summary to stdout for programmatic consumption."""
    summary = {
        'total': len(results),
        'new': sum(1 for r in results if r['status'] == 'new'),
        'unchanged': sum(1 for r in results if r['status'] == 'unchanged'),
        'updated': sum(1 for r in results if r['status'] == 'updated'),
        'errors': sum(1 for r in results if r['status'] == 'error'),
        'articles': results
    }
    print(json.dumps(summary))


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Sync blog articles from ERPNext with fidelity checking'
    )
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show what would happen without writing files')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Force overwrite all files, ignoring fidelity check')
    parser.add_argument('--list', '-l', action='store_true',
                        help='Only list available blogs, do not sync')
    parser.add_argument('--skip-images', action='store_true',
                        help='Skip downloading images')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show verbose output')
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    content_dir = script_dir.parent / 'content' / 'blog'
    static_dir = script_dir.parent / 'static'

    if not content_dir.exists():
        print(f"Error: Content directory not found: {content_dir}", file=sys.stderr)
        sys.exit(2)

    print(f"Fetching blog list from {ERPNEXT_URL}...", file=sys.stderr)
    blogs = fetch_blog_list()

    if not blogs:
        print("No blogs found or error occurred.", file=sys.stderr)
        sys.exit(2)

    print(f"Found {len(blogs)} published blogs", file=sys.stderr)

    if args.list:
        # Just list the blogs
        results = []
        for blog in blogs:
            results.append({
                'title': blog.get('title', 'Untitled'),
                'date': str(blog.get('published_on', ''))[:10],
                'author': blog.get('blogger', 'Unknown'),
                'status': 'available',
                'fidelity': '-'
            })
        print_status_table(results, dry_run=True)
        return

    results = []
    errors_occurred = False

    for i, blog in enumerate(blogs):
        blog_name = blog.get('name')
        if not blog_name:
            continue

        # Fetch full blog content by scraping the web page (has proper HTML formatting)
        if args.verbose:
            print(f"Fetching {i+1}/{len(blogs)}: {blog.get('title', 'Untitled')}", file=sys.stderr)
        blog_detail = fetch_blog_detail(blog_name)
        if not blog_detail:
            results.append({
                'title': blog.get('title', 'Untitled'),
                'date': str(blog.get('published_on', ''))[:10],
                'author': blog.get('blogger', 'Unknown'),
                'status': 'error',
                'fidelity': '-',
                'file': ''
            })
            errors_occurred = True
            continue

        # Sync the blog
        sync_result = sync_blog(
            blog_detail, content_dir, static_dir,
            dry_run=args.dry_run, force=args.force,
            skip_images=args.skip_images, verbose=args.verbose
        )

        results.append({
            'title': blog.get('title', 'Untitled'),
            'date': str(blog.get('published_on', ''))[:10],
            'author': blog.get('blogger', 'Unknown'),
            'status': sync_result['status'],
            'fidelity': sync_result['fidelity'],
            'file': sync_result.get('file', '')
        })

    # Output results
    print_status_table(results, dry_run=args.dry_run)

    # Exit code based on errors
    if errors_occurred:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
