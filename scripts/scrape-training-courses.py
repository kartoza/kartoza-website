#!/usr/bin/env python3
"""
Scrape training course information from ERPNext website using web scraping.

This script scrapes:
- Training course pages from ERPNext shop
- Course descriptions, prices, schedules
- Course images

The script uses web scraping to extract course content from HTML pages.
A minimal API call is used to discover course routes (since the listing
pages use JavaScript rendering). Optionally, variant/scheduling data can
also be fetched via API using --fetch-variants.

Usage:
    python3 scrape-training-courses.py              # Full sync
    python3 scrape-training-courses.py --dry-run    # Preview changes
    python3 scrape-training-courses.py --list       # List available courses
    python3 scrape-training-courses.py --force      # Force overwrite all
    python3 scrape-training-courses.py --verbose    # Verbose output
    python3 scrape-training-courses.py --fetch-variants  # Also fetch dates/venues

Environment variables:
    ERPNEXT_URL - Base URL for ERPNext (default: https://erp.kartoza.com)
"""

import os
import sys
import re
import json
import argparse
import warnings
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from tabulate import tabulate

# Suppress XML parsing warning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Configuration
ERPNEXT_URL = os.environ.get("ERPNEXT_URL", "https://erp.kartoza.com")
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
TRAINING_CONTENT_DIR = PROJECT_ROOT / "content" / "training-courses"
CALENDAR_DATA_DIR = PROJECT_ROOT / "data" / "training"
STATIC_DIR = PROJECT_ROOT / "static"
IMAGE_DIR = "img/training/erpnext"

# Fallback course URL patterns (used if route discovery fails)
FALLBACK_COURSE_PATHS = [
    "shop/product/introduction-to-qgis",
]


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')


def truncate_at_sentence(text: str, max_length: int = 200) -> str:
    """Truncate text at a sentence boundary."""
    if not text or len(text) <= max_length:
        return text

    truncated = text[:max_length]

    for punct in ['. ', '! ', '? ']:
        last_punct = truncated.rfind(punct)
        if last_punct > max_length // 2:
            return truncated[:last_punct + 1].strip()

    last_space = truncated.rfind(' ')
    if last_space > max_length // 2:
        return truncated[:last_space].strip() + '...'

    return truncated.strip() + '...'


def clean_html_to_text(html: str) -> str:
    """Convert HTML to clean text."""
    if not html:
        return ""

    soup = BeautifulSoup(html, 'html.parser')

    # Remove script and style elements
    for element in soup(['script', 'style']):
        element.decompose()

    text = soup.get_text(separator=' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def html_to_markdown(html: str) -> str:
    """Convert HTML to markdown-friendly text."""
    if not html:
        return ""

    text = html

    # Handle line breaks and paragraphs
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'</p>\s*<p[^>]*>', '\n\n', text)
    text = re.sub(r'<p[^>]*>', '', text)
    text = re.sub(r'</p>', '\n\n', text)

    # Handle lists
    text = re.sub(r'<li[^>]*>', '- ', text)
    text = re.sub(r'</li>', '\n', text)
    text = re.sub(r'</?[ou]l[^>]*>', '\n', text)

    # Handle headings
    text = re.sub(r'<h1[^>]*>', '# ', text)
    text = re.sub(r'<h2[^>]*>', '## ', text)
    text = re.sub(r'<h3[^>]*>', '### ', text)
    text = re.sub(r'</h[123456]>', '\n\n', text)

    # Handle bold/italic
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text)

    # Handle HTML entities
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    text = text.replace('&ndash;', '–')
    text = text.replace('&mdash;', '—')

    # Strip remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' +', ' ', text)

    return text.strip()


def download_image(url: str, verbose: bool = False) -> str | None:
    """Download an image and return local path."""
    if not url:
        return None

    # Normalize URL
    if url.startswith('/'):
        full_url = f"{ERPNEXT_URL}{url}"
    elif not url.startswith('http'):
        full_url = f"{ERPNEXT_URL}/{url}"
    else:
        full_url = url

    # Extract filename
    parsed = urlparse(full_url)
    filename = os.path.basename(parsed.path)
    if not filename:
        return None

    # Create target directory
    target_dir = STATIC_DIR / IMAGE_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / filename
    local_url = f"/{IMAGE_DIR}/{filename}"

    # Skip if already downloaded
    if target_path.exists():
        if verbose:
            print(f"  Image exists: {filename}")
        return local_url

    # Download the image
    try:
        if verbose:
            print(f"  Downloading: {filename}")
        response = requests.get(full_url, timeout=30)
        response.raise_for_status()
        target_path.write_bytes(response.content)
        return local_url
    except requests.RequestException as e:
        print(f"  Warning: Failed to download {full_url}: {e}", file=sys.stderr)
        return None


def scrape_course_page(url: str, verbose: bool = False) -> dict | None:
    """Scrape a single course page and extract information."""
    if verbose:
        print(f"  Scraping: {url}")

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 404:
            if verbose:
                print(f"  Not found: {url}")
            return None
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  Error fetching {url}: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract course information
    course = {
        'url': url,
        'slug': url.split('/')[-1],
    }

    # Title - look for various selectors
    title_selectors = [
        'h1.product-title',
        '.product-title',
        'h1[itemprop="name"]',
        '.item-title h1',
        'h1',
    ]
    for selector in title_selectors:
        title_elem = soup.select_one(selector)
        if title_elem:
            course['title'] = title_elem.get_text(strip=True)
            break
    else:
        course['title'] = course['slug'].replace('-', ' ').title()

    # Price
    price_selectors = [
        '.product-price',
        '[itemprop="price"]',
        '.item-price',
        '.price',
    ]
    for selector in price_selectors:
        price_elem = soup.select_one(selector)
        if price_elem:
            price_text = price_elem.get_text(strip=True)
            # Clean up price text
            price_match = re.search(r'R?\s*[\d,]+(?:\.\d{2})?', price_text)
            if price_match:
                course['price'] = price_match.group(0)
            break

    # Description - look for product description
    desc_selectors = [
        '.product-description',
        '[itemprop="description"]',
        '.item-description',
        '.web-long-description',
        '.item-content',
    ]
    for selector in desc_selectors:
        desc_elem = soup.select_one(selector)
        if desc_elem:
            course['description_html'] = str(desc_elem)
            course['description'] = html_to_markdown(str(desc_elem))
            break

    # Short description
    short_desc_selectors = [
        '.short-description',
        '.product-summary',
        'meta[name="description"]',
    ]
    for selector in short_desc_selectors:
        if selector.startswith('meta'):
            elem = soup.select_one(selector)
            if elem and elem.get('content'):
                course['short_description'] = elem['content']
                break
        else:
            elem = soup.select_one(selector)
            if elem:
                course['short_description'] = clean_html_to_text(str(elem))
                break

    if 'short_description' not in course and 'description' in course:
        course['short_description'] = truncate_at_sentence(
            clean_html_to_text(course.get('description', '')), 200
        )

    # Duration - look for duration info
    duration_patterns = [
        r'(\d+)\s*days?',
        r'(\d+)\s*hours?',
        r'duration[:\s]+([^<\n]+)',
    ]
    page_text = soup.get_text()
    for pattern in duration_patterns:
        match = re.search(pattern, page_text, re.I)
        if match:
            if 'day' in pattern:
                course['duration'] = f"{match.group(1)} Days"
            elif 'hour' in pattern:
                course['duration'] = f"{match.group(1)} Hours"
            else:
                course['duration'] = match.group(1).strip()
            break

    # Image - look for product image
    img_selectors = [
        '.product-image img',
        '[itemprop="image"]',
        '.item-image img',
        '.product-img img',
        'img.product',
    ]
    for selector in img_selectors:
        img_elem = soup.select_one(selector)
        if img_elem:
            img_url = img_elem.get('src') or img_elem.get('data-src')
            if img_url:
                course['image_url'] = img_url
                break

    # Item code - look for data attributes (needed for variant fetching)
    item_code_elem = soup.select_one('[data-item-code]')
    if item_code_elem:
        course['item_code'] = item_code_elem.get('data-item-code')

    # Scheduled dates/variants - look for date options
    date_selectors = [
        '.variant-selector option',
        '[data-attribute*="date"] option',
        '.date-option',
    ]
    dates = []
    for selector in date_selectors:
        for elem in soup.select(selector):
            date_text = elem.get_text(strip=True)
            if date_text and re.search(r'\d{1,2}.*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', date_text, re.I):
                dates.append(date_text)
    if dates:
        course['dates'] = dates

    # Venue/location options
    venue_selectors = [
        '[data-attribute*="venue"] option',
        '[data-attribute*="location"] option',
        '.venue-option',
    ]
    venues = []
    for selector in venue_selectors:
        for elem in soup.select(selector):
            venue_text = elem.get_text(strip=True)
            if venue_text and venue_text.lower() not in ['select', 'choose', '']:
                venues.append(venue_text)
    if venues:
        course['venues'] = venues

    return course


def fetch_item_variants(item_code: str, verbose: bool = False) -> dict:
    """
    Fetch variant attributes (dates/venues) for a course item.

    This is an optional API call to get scheduling data that isn't
    available in the static HTML pages.
    """
    try:
        url = f"{ERPNEXT_URL}/api/method/webshop.webshop.variant_selector.utils.get_attributes_and_values"
        params = {"item_code": item_code}
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json().get("message", [])
    except requests.RequestException:
        pass
    return []


def get_variants_for_course(item_code: str, verbose: bool = False) -> tuple[list, list]:
    """Get dates and venues for a course from variant data."""
    variants = fetch_item_variants(item_code, verbose)
    dates = []
    venues = []

    for attr in variants:
        attr_name = (attr.get("attribute") or "").lower()
        values = attr.get("values", [])

        if "date" in attr_name:
            dates = values
        elif "venue" in attr_name or "location" in attr_name:
            venues = values

    if not venues:
        venues = ["Online"]

    return dates, venues


def discover_routes_from_api(verbose: bool = False) -> list[dict]:
    """
    Discover training course routes using minimal API call.

    This is the only API call - just to get the list of URLs.
    All content extraction is done via web scraping.
    """
    routes = []

    try:
        url = f"{ERPNEXT_URL}/api/resource/Website%20Item"
        params = {
            "limit_page_length": 100,
            "fields": '["name","route","item_group","published","web_item_name"]'
        }

        if verbose:
            print("  Fetching route list from API...")

        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json().get("data", [])
            for item in data:
                item_group = (item.get("item_group") or "").lower()
                # Only include training-related items that are published
                if "training" in item_group and item.get("published"):
                    route = item.get("route", "")
                    if route:
                        routes.append({
                            "route": route,
                            "name": item.get("web_item_name") or item.get("name", ""),
                        })
                        if verbose:
                            print(f"    Found: {route}")

    except requests.RequestException as e:
        if verbose:
            print(f"  API error (will use fallbacks): {e}")

    return routes


def discover_courses_from_page(verbose: bool = False) -> list[str]:
    """Try to discover course URLs from the training page."""
    discovered = []

    # Try the all-products page with training filter
    urls_to_try = [
        f"{ERPNEXT_URL}/all-products?item_group=Training",
        f"{ERPNEXT_URL}/training-courses",
        f"{ERPNEXT_URL}/training",
    ]

    for page_url in urls_to_try:
        try:
            if verbose:
                print(f"  Checking: {page_url}")
            response = requests.get(page_url, timeout=30)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for product links
            for link in soup.find_all('a', href=True):
                href = link['href']
                if '/shop/product/' in href or '/training/' in href:
                    full_url = urljoin(ERPNEXT_URL, href)
                    if full_url not in discovered:
                        discovered.append(full_url)

        except requests.RequestException as e:
            if verbose:
                print(f"  Error: {e}")
            continue

    return discovered


def get_known_course_urls(verbose: bool = False) -> list[dict]:
    """
    Get list of known course URLs from various sources.

    Returns list of dicts with 'url' and 'name' keys.
    """
    courses = {}  # route -> {url, name}

    # First, try to discover routes from API (just URLs, not content)
    api_routes = discover_routes_from_api(verbose=verbose)
    for item in api_routes:
        route = item['route']
        url = f"{ERPNEXT_URL}/{route}"
        courses[route] = {'url': url, 'name': item['name']}

    # Add fallback paths if API returned nothing
    if not courses:
        for path in FALLBACK_COURSE_PATHS:
            url = f"{ERPNEXT_URL}/{path}"
            courses[path] = {'url': url, 'name': path.split('/')[-1]}

    # Also check existing events.json for any additional URLs
    events_file = CALENDAR_DATA_DIR / "events.json"
    if events_file.exists():
        try:
            events = json.loads(events_file.read_text())
            for event in events:
                reg_url = event.get('registration_url', '')
                if reg_url:
                    # Extract route from URL
                    parsed = urlparse(reg_url)
                    route = parsed.path.lstrip('/')
                    if route and route not in courses:
                        courses[route] = {
                            'url': reg_url,
                            'name': event.get('title', route.split('/')[-1])
                        }
        except (json.JSONDecodeError, IOError):
            pass

    return list(courses.values())


def read_local_course(filepath: Path) -> tuple[dict, str] | None:
    """Read a local Hugo course file."""
    if not filepath.exists():
        return None

    try:
        text = filepath.read_text()
    except (IOError, OSError):
        return None

    if not text.startswith('---'):
        return {}, text

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


def find_local_course(slug: str) -> Path | None:
    """Find a local course file by slug."""
    if not TRAINING_CONTENT_DIR.exists():
        return None

    # Direct match
    direct_path = TRAINING_CONTENT_DIR / f"{slug}.md"
    if direct_path.exists():
        return direct_path

    # Try variations
    variations = [
        slug,
        slug.replace('-', ''),
        re.sub(r'-+', '-', slug),
    ]

    for var in variations:
        path = TRAINING_CONTENT_DIR / f"{var}.md"
        if path.exists():
            return path

    # Search by shop_url in frontmatter
    for md_file in TRAINING_CONTENT_DIR.glob('*.md'):
        if md_file.name == '_index.md':
            continue
        result = read_local_course(md_file)
        if result:
            fm, _ = result
            shop_url = fm.get('shop_url', '')
            if slug in shop_url:
                return md_file

    return None


def normalize_for_comparison(content: str) -> str:
    """Normalize content for fidelity comparison."""
    if not content:
        return ''

    # Remove Hugo shortcodes
    content = re.sub(r'\{\{[<>%].*?[>%]\}\}', '', content)

    # Strip HTML tags
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text(separator=' ')

    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip().lower()


def check_fidelity(local_content: str, scraped_content: str) -> bool:
    """Check if local and scraped content match."""
    local_norm = normalize_for_comparison(local_content)
    scraped_norm = normalize_for_comparison(scraped_content)

    # Allow some flexibility - check if significant content matches
    if not local_norm or not scraped_norm:
        return False

    # Check if at least 80% of words match
    local_words = set(local_norm.split())
    scraped_words = set(scraped_norm.split())

    if not scraped_words:
        return True

    overlap = len(local_words & scraped_words)
    match_ratio = overlap / len(scraped_words)

    return match_ratio > 0.7


def create_course_page(course: dict, dry_run: bool = False, force: bool = False,
                        skip_images: bool = False, verbose: bool = False) -> dict:
    """Create or update a training course page."""
    slug = course.get('slug') or slugify(course.get('title', 'unknown'))
    # Clean slug
    slug = slug.replace('shop-product-', '').replace('training-', '')
    # Remove random suffixes
    if '-' in slug:
        parts = slug.rsplit('-', 1)
        if len(parts) > 1 and len(parts[1]) == 5 and parts[1].isalnum():
            slug = parts[0]

    local_file = find_local_course(slug)
    filepath = local_file if local_file else TRAINING_CONTENT_DIR / f"{slug}.md"

    # Check if we should update
    if local_file and not force:
        result = read_local_course(local_file)
        if result:
            local_fm, local_content = result

            # Check fidelity
            scraped_desc = course.get('description', '')
            if check_fidelity(local_content, scraped_desc):
                # Content matches - just update review fields if needed
                if not local_fm.get('reviewedBy'):
                    if not dry_run:
                        local_fm['reviewedBy'] = 'Automated Scrape'
                        local_fm['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')
                        file_content = "---\n"
                        file_content += yaml.dump(local_fm, default_flow_style=False, allow_unicode=True)
                        file_content += "---\n\n"
                        file_content += local_content.strip()
                        file_content += "\n"
                        filepath.write_text(file_content)
                return {'status': 'unchanged', 'fidelity': 'passed', 'file': filepath.name}

            status = 'updated'
        else:
            status = 'new'
    elif local_file and force:
        status = 'forced'
    else:
        status = 'new'

    # Download image
    thumbnail = f"/img/training/{slug}.jpg"
    if not skip_images and course.get('image_url'):
        local_img = download_image(course['image_url'], verbose=verbose)
        if local_img:
            thumbnail = local_img

    # Build frontmatter
    title = course.get('title', slug.replace('-', ' ').title())
    short_desc = course.get('short_description', '')
    if not short_desc and course.get('description'):
        short_desc = truncate_at_sentence(clean_html_to_text(course['description']), 200)

    # Escape quotes
    short_desc_escaped = short_desc.replace('"', '\\"')
    title_escaped = title.replace('"', '\\"')

    shop_url = course.get('url', f"{ERPNEXT_URL}/shop/product/{slug}")

    front_matter = {
        'title': title,
        'description': short_desc_escaped,
        'thumbnail': thumbnail,
        'shop_url': shop_url,
        'tags': ['Training'],
        'draft': False,
        'reviewedBy': 'Automated Scrape',
        'reviewedDate': datetime.now().strftime('%Y-%m-%d'),
    }

    if course.get('duration'):
        front_matter['duration'] = course['duration']
    if course.get('price'):
        front_matter['price'] = course['price']

    # Build content
    description = course.get('description', 'Course overview coming soon.')

    content = f'''---
title: "{title_escaped}"
description: "{short_desc_escaped}"
thumbnail: "{thumbnail}"
shop_url: "{shop_url}"
tags:
  - Training
draft: false
reviewedBy: "Tim Sutton"
reviewedDate: {datetime.now().strftime('%Y-%m-%d')}
---

{{{{< block
    title="{title_escaped}"
    subtitle="Professional GIS Training"
    class="is-primary"
    sub-block-side="bottom"
>}}}}
{short_desc or 'Professional training course from Kartoza.'}
{{{{< /block >}}}}

## Overview

{description}

<!-- markdownlint-disable MD034 -->
{{{{< button-bar "fas fa-shopping-cart:Book This Course:{shop_url}" "fas fa-envelope:Enquire:/contact-us/" >}}}}
<!-- markdownlint-enable MD034 -->
'''

    if dry_run:
        print(f"  Would write: {filepath.name}")
    else:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
        if verbose:
            print(f"  Wrote: {filepath.name}")

    return {'status': status, 'fidelity': 'auto-reviewed', 'file': filepath.name}


def parse_date_range(date_str: str) -> tuple:
    """Parse date range into start and end dates."""
    months = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }

    # Pattern: "12 - 14 May 2026"
    match = re.match(r'(\d{1,2})\s*[-–]\s*(\d{1,2})\s+(\w+)\s+(\d{4})', date_str)
    if match:
        start_day, end_day, month, year = match.groups()
        month_num = months.get(month.lower(), 1)
        start_date = f"{year}-{month_num:02d}-{int(start_day):02d}"
        end_date = f"{year}-{month_num:02d}-{int(end_day):02d}"
        return start_date, end_date

    # Pattern: "29 June 2026 to 10 July 2026"
    match = re.match(r'(\d{1,2})\s+(\w+)\s+(\d{4})\s+to\s+(\d{1,2})\s+(\w+)\s+(\d{4})', date_str, re.I)
    if match:
        start_day, start_month, start_year, end_day, end_month, end_year = match.groups()
        start_month_num = months.get(start_month.lower(), 1)
        end_month_num = months.get(end_month.lower(), 1)
        start_date = f"{start_year}-{start_month_num:02d}-{int(start_day):02d}"
        end_date = f"{end_year}-{end_month_num:02d}-{int(end_day):02d}"
        return start_date, end_date

    # Single date: "12 May 2026"
    match = re.match(r'(\d{1,2})\s+(\w+)\s+(\d{4})', date_str)
    if match:
        day, month, year = match.groups()
        month_num = months.get(month.lower(), 1)
        date = f"{year}-{month_num:02d}-{int(day):02d}"
        return date, date

    return None, None


def clean_slug_for_hugo(raw_slug: str) -> str:
    """Clean up a slug for use in Hugo URLs."""
    slug = raw_slug

    # Remove path prefixes
    for prefix in ['shop/product/', 'training/', 'training-courses/']:
        if slug.startswith(prefix):
            slug = slug[len(prefix):]

    # Remove random 5-char suffixes (e.g., -7ihjm, -ypfsx)
    if '-' in slug:
        parts = slug.rsplit('-', 1)
        if len(parts) > 1 and len(parts[1]) == 5 and parts[1].isalnum():
            slug = parts[0]

    return slug


def save_calendar_data(courses: list[dict], dry_run: bool = False) -> list[dict]:
    """Save scraped session data to calendar JSON."""
    calendar_events = []

    for course in courses:
        dates = course.get('dates', [])
        venues = course.get('venues', ['Online'])
        raw_slug = course.get('slug', '')
        clean_slug = clean_slug_for_hugo(raw_slug)
        title = course.get('title', 'Training')
        shop_url = course.get('url', '')

        for date_str in dates:
            start_date, end_date = parse_date_range(date_str)
            if start_date:
                for venue in venues:
                    calendar_events.append({
                        "title": title,
                        "start": start_date,
                        "end": end_date,
                        "date_display": date_str,
                        "location": venue.title() if venue else "Online",
                        "url": f"/training-courses/{clean_slug}/",
                        "registration_url": shop_url,
                    })

    if calendar_events:
        CALENDAR_DATA_DIR.mkdir(parents=True, exist_ok=True)
        data_file = CALENDAR_DATA_DIR / "events.json"

        if dry_run:
            print(f"Would save {len(calendar_events)} events to: {data_file}")
        else:
            data_file.write_text(json.dumps(calendar_events, indent=2))
            print(f"Saved {len(calendar_events)} events to: {data_file}")

    return calendar_events


def list_courses(verbose: bool = False):
    """List all available courses."""
    print("=" * 70)
    print("Training Courses - Web Scraping")
    print("=" * 70)

    # Get known URLs (uses API to discover routes, then we scrape content)
    print("\nDiscovering course routes...")
    course_info = get_known_course_urls(verbose=verbose)
    print(f"Found {len(course_info)} course URLs")

    print(f"\nScraping {len(course_info)} courses...")
    print("-" * 50)

    results = []
    for info in course_info:
        url = info['url']
        course = scrape_course_page(url, verbose=verbose)
        if course:
            results.append(course)
            title = course.get('title', 'Unknown')
            price = course.get('price', 'N/A')
            duration = course.get('duration', 'N/A')
            dates = len(course.get('dates', []))
            print(f"  {title}")
            print(f"      URL: {url}")
            print(f"      Price: {price}, Duration: {duration}, Sessions: {dates}")
        else:
            # Use name from API if scraping failed
            print(f"  {info['name']} (scrape failed)")
            print(f"      URL: {url}")

    print(f"\nSuccessfully scraped: {len(results)} courses")

    print("\nLocal Courses:")
    print("-" * 50)
    if TRAINING_CONTENT_DIR.exists():
        for md_file in sorted(TRAINING_CONTENT_DIR.glob('*.md')):
            if md_file.name != '_index.md':
                print(f"  - {md_file.stem}")

    print("\n" + "=" * 70)


def sync_courses(dry_run: bool = False, force: bool = False,
                 skip_images: bool = False, verbose: bool = False,
                 fetch_variants: bool = False):
    """Sync all training courses from ERPNext."""
    print("=" * 70)
    print("Syncing Training Courses via Web Scraping")
    print("=" * 70)

    # Get URLs (uses API to discover routes, then scrapes content)
    print("\nGathering course URLs...")
    course_info = get_known_course_urls(verbose=verbose)
    print(f"Found {len(course_info)} course URLs to scrape")

    if fetch_variants:
        print("  (Will also fetch scheduling variants via API)")

    # Scrape each course
    print("\nScraping courses...")
    courses = []
    results = []

    for info in course_info:
        url = info['url']
        course = scrape_course_page(url, verbose=verbose)
        if course:
            # Optionally fetch variant data (dates/venues) via API
            if fetch_variants:
                # Try to get item_code from the page
                item_code = course.get('item_code')
                if not item_code:
                    # Try to extract from data attributes in the scraped HTML
                    # or use the course title as fallback
                    item_code = info.get('name', course.get('title', ''))

                if item_code:
                    dates, venues = get_variants_for_course(item_code, verbose)
                    if dates:
                        course['dates'] = dates
                    if venues:
                        course['venues'] = venues
                    if verbose and dates:
                        print(f"    Found {len(dates)} date(s) for {course.get('title')}")

            courses.append(course)
            result = create_course_page(
                course,
                dry_run=dry_run,
                force=force,
                skip_images=skip_images,
                verbose=verbose
            )
            results.append(result)
        elif verbose:
            print(f"  Skipped (scrape failed): {info['name']}")

    # Summary table
    if results:
        print("\nResults:")
        print("-" * 50)
        table_data = []
        for r in results:
            table_data.append([r['file'], r['status'], r.get('fidelity', '')])
        print(tabulate(table_data, headers=['File', 'Status', 'Fidelity']))

    # Save calendar data
    print("\nUpdating calendar data...")
    save_calendar_data(courses, dry_run=dry_run)

    # Summary
    status_counts = {}
    for r in results:
        s = r['status']
        status_counts[s] = status_counts.get(s, 0) + 1

    print("\nSummary:")
    for status, count in status_counts.items():
        print(f"  {status}: {count}")

    print("\n" + "=" * 70)
    print("Done!")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Scrape training courses from ERPNext website"
    )
    parser.add_argument("--list", action="store_true",
                        help="List available courses without syncing")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without writing files")
    parser.add_argument("--force", action="store_true",
                        help="Force overwrite all files")
    parser.add_argument("--skip-images", action="store_true",
                        help="Skip downloading images")
    parser.add_argument("--fetch-variants", action="store_true",
                        help="Fetch scheduling variants (dates/venues) via API")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")

    args = parser.parse_args()

    if args.list:
        list_courses(verbose=args.verbose)
    else:
        sync_courses(
            dry_run=args.dry_run,
            force=args.force,
            skip_images=args.skip_images,
            verbose=args.verbose,
            fetch_variants=args.fetch_variants
        )


if __name__ == "__main__":
    main()
