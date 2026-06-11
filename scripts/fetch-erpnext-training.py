#!/usr/bin/env python3
"""
Fetch training course information and scheduled events from ERPNext.

This script uses the ERPNext API to fetch:
- Training courses from Website Items
- Scheduled sessions (variants) with dates and venues

Usage:
    python3 fetch-erpnext-training.py [--list] [--dry-run]

Environment variables:
    ERPNEXT_URL - Base URL for ERPNext (default: https://erp.kartoza.com)

Options:
    --list      List training courses and scheduled sessions
    --dry-run   Preview changes without writing files
"""

import os
import sys
import re
import json
import argparse
import requests
import yaml
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

# ERPNext configuration
ERPNEXT_URL = os.environ.get("ERPNEXT_URL", "https://erp.kartoza.com")
TRAINING_CONTENT_DIR = Path(__file__).parent.parent / "content" / "training-courses"
CALENDAR_DATA_DIR = Path(__file__).parent.parent / "data" / "training"


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text


def normalize_for_comparison(content: str) -> str:
    """
    Normalize content for fidelity comparison.
    Focuses on TEXT content, ignores formatting/layout.
    """
    if not content:
        return ''

    # Remove Hugo shortcodes
    content = re.sub(r'\{\{[<>%].*?[>%]\}\}', '', content)

    # Strip HTML tags but keep text content
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text(separator=' ')

    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text)

    return text.strip().lower()


def check_fidelity(local_content: str, erpnext_content: str) -> bool:
    """
    Check if local and ERPNext content match (fidelity check).

    Returns True if text content matches (ignoring formatting).
    """
    local_norm = normalize_for_comparison(local_content)
    erpnext_norm = normalize_for_comparison(erpnext_content)
    return local_norm == erpnext_norm


def read_local_file(filepath: Path) -> tuple[dict, str] | None:
    """Read a local Hugo file and extract front matter and content."""
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


def truncate_at_sentence(text: str, max_length: int = 200) -> str:
    """Truncate text at a sentence boundary, not mid-word."""
    if not text or len(text) <= max_length:
        return text

    # Find the last sentence-ending punctuation before max_length
    truncated = text[:max_length]

    # Try to find a sentence boundary (. ! ?)
    for punct in ['. ', '! ', '? ']:
        last_punct = truncated.rfind(punct)
        if last_punct > max_length // 2:  # At least halfway through
            return truncated[:last_punct + 1].strip()

    # Fall back to last space to avoid mid-word cut
    last_space = truncated.rfind(' ')
    if last_space > max_length // 2:
        return truncated[:last_space].strip() + '...'

    return truncated.strip() + '...'


def clean_html_to_markdown(html: str) -> str:
    """Convert HTML to clean markdown-friendly text."""
    if not html:
        return ""

    # Replace common HTML elements with markdown equivalents
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
    text = text.strip()

    return text


def parse_date_range(date_str: str) -> tuple:
    """Parse date range into start and end dates."""
    months = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }

    # Pattern: "12 - 14 May 2026" or "12-14 May 2026" (same month)
    match = re.match(r'(\d{1,2})\s*[-–]\s*(\d{1,2})\s+(\w+)\s+(\d{4})', date_str)
    if match:
        start_day, end_day, month, year = match.groups()
        month_num = months.get(month.lower(), 1)
        start_date = f"{year}-{month_num:02d}-{int(start_day):02d}"
        end_date = f"{year}-{month_num:02d}-{int(end_day):02d}"
        return start_date, end_date

    # Pattern: "29 June 2026 to 10 July 2026" (different months)
    match = re.match(r'(\d{1,2})\s+(\w+)\s+(\d{4})\s+to\s+(\d{1,2})\s+(\w+)\s+(\d{4})', date_str, re.I)
    if match:
        start_day, start_month, start_year, end_day, end_month, end_year = match.groups()
        start_month_num = months.get(start_month.lower(), 1)
        end_month_num = months.get(end_month.lower(), 1)
        start_date = f"{start_year}-{start_month_num:02d}-{int(start_day):02d}"
        end_date = f"{end_year}-{end_month_num:02d}-{int(end_day):02d}"
        return start_date, end_date

    # Pattern: "16 - 27 February 2026" (with spaces around dash)
    match = re.match(r'(\d{1,2})\s*[-–]\s*(\d{1,2})\s+(\w+)\s+(\d{4})', date_str)
    if match:
        start_day, end_day, month, year = match.groups()
        month_num = months.get(month.lower(), 1)
        start_date = f"{year}-{month_num:02d}-{int(start_day):02d}"
        end_date = f"{year}-{month_num:02d}-{int(end_day):02d}"
        return start_date, end_date

    # Single date pattern: "12 May 2026"
    match = re.match(r'(\d{1,2})\s+(\w+)\s+(\d{4})', date_str)
    if match:
        day, month, year = match.groups()
        month_num = months.get(month.lower(), 1)
        date = f"{year}-{month_num:02d}-{int(day):02d}"
        return date, date

    return None, None


def fetch_website_items() -> list:
    """Fetch all Website Items from ERPNext."""
    try:
        url = f"{ERPNEXT_URL}/api/resource/Website%20Item"
        params = {
            "limit_page_length": 100,
            "fields": json.dumps([
                "name", "web_item_name", "item_code", "item_name",
                "item_group", "route", "published", "short_description"
            ])
        }
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json().get("data", [])
    except Exception as e:
        print(f"Error fetching Website Items: {e}")
    return []


def fetch_website_item_details(item_name: str) -> dict:
    """Fetch detailed information for a specific Website Item."""
    try:
        url = f"{ERPNEXT_URL}/api/resource/Website%20Item/{item_name}"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json().get("data", {})
    except Exception as e:
        print(f"  Warning: Could not fetch details for {item_name}: {e}")
    return {}


def fetch_item_variants(item_code: str) -> dict:
    """Fetch variant attributes (dates/venues) for an item."""
    try:
        url = f"{ERPNEXT_URL}/api/method/kartoza_custom.api.get_attributes_and_values"
        params = {"item_code": item_code}
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json().get("message", [])
    except Exception as e:
        pass  # Item may not have variants
    return []


def pick_zar_price(prices: list) -> tuple:
    """Return (price_list_rate, currency) preferring the most recent ZAR price.

    When multiple ZAR entries exist (e.g. "2024 Standard Selling - ZAR",
    "2026 Standard Selling - ZAR"), the one with the highest year in the
    price_list name wins. Falls back to the first price in any currency.
    """
    if not prices:
        return None, None
    zar_prices = [p for p in prices if p.get("currency") == "ZAR"]
    if zar_prices:
        def year_key(p):
            m = re.search(r'\b(\d{4})\b', p.get("price_list", ""))
            return int(m.group(1)) if m else 0
        best = max(zar_prices, key=year_key)
        return best.get("price_list_rate"), "ZAR"
    first = prices[0]
    return first.get("price_list_rate"), first.get("currency")


def get_active_items_with_variants() -> list:
    """Fetch all active (published) training website items with their variants and prices.

    Prices are sourced from get_attributes_and_values, which returns per-variant
    price lists. The course-level price prefers ZAR; falls back to the first available.
    """
    items = fetch_website_items()
    result = []

    for item in items:
        if not item.get("published"):
            continue

        item_group = item.get("item_group", "").lower()
        if "training" not in item_group and "course" not in item_group:
            continue

        item_code = item.get("item_code") or item.get("item_name", "")
        details = fetch_website_item_details(item.get("name", ""))
        variants = fetch_item_variants(item_code)

        # Derive course-level price from variant prices returned by get_attributes_and_values
        all_prices = [p for v in variants for p in v.get("prices", [])]
        price, price_currency = pick_zar_price(all_prices)

        raw_slug = item.get("route", "").replace("shop/product/", "")
        clean_slug = raw_slug.replace("training/", "").replace("training-courses/", "")
        if "-" in clean_slug:
            parts = clean_slug.rsplit("-", 1)
            if len(parts) > 1 and len(parts[1]) == 5 and parts[1].isalnum():
                clean_slug = parts[0]

        result.append({
            "name": item.get("web_item_name") or item.get("item_name", ""),
            "item_code": item_code,
            "slug": clean_slug,
            "raw_slug": raw_slug,
            "short_description": item.get("short_description", ""),
            "description": details.get("web_long_description", item.get("short_description", "")),
            "published": item.get("published", 0),
            "price": price,
            "price_currency": price_currency,
            "variants": variants,
        })

    return result


def fetch_training_courses() -> list:
    """Fetch all active training courses from ERPNext."""
    return get_active_items_with_variants()


def fetch_all_scheduled_sessions() -> list:
    """Fetch all scheduled training sessions (variants) from ERPNext."""
    courses = get_active_items_with_variants()
    all_sessions = []

    for course in courses:
        item_code = course.get("item_code", "")
        if not item_code:
            continue

        variants = course.get("variants", [])
        if not variants:
            continue

        for attr in variants:
            if not attr.get("variants", {}):
                continue

            display_date = attr['variants']['Date']
            variant_code = attr['item_code']
            venue = attr['variants']['Venue']
            if not display_date or not venue:
                continue

            start_date, end_date = parse_date_range(display_date)
            if not start_date:
                continue

            if start_date <= datetime.today().strftime("%Y-%m-%d"):
                continue

            variant_price, variant_currency = pick_zar_price(attr.get("prices", []))

            all_sessions.append({
                "course_name": course.get("name", ""),
                "course_slug": course.get("slug", ""),
                "item_code": variant_code,
                "date_display": display_date,
                "start_date": start_date,
                "end_date": end_date,
                "location": venue.title() if venue else "Online",
                "price": variant_price,
                "price_currency": variant_currency,
                "shop_url": f"{ERPNEXT_URL}/shop/product/{course.get('raw_slug', course.get('slug', ''))}"
            })
    all_sessions.sort(key=lambda s: s["start_date"])
    return all_sessions


def get_existing_courses() -> dict:
    """Get existing course files."""
    courses = {}
    if not TRAINING_CONTENT_DIR.exists():
        return courses

    for md_file in TRAINING_CONTENT_DIR.glob("*.md"):
        if md_file.name == "_index.md":
            continue
        courses[md_file.stem] = {"file": md_file, "slug": md_file.stem}

    return courses


def create_course_page(course: dict, dry_run: bool = False) -> Path:
    """Create or update a training course page with fidelity checking."""
    slug = course.get("slug") or slugify(course.get("name", "unknown"))
    # Remove any path prefixes from slug
    slug = slug.replace("shop/product/", "").replace("training/", "").replace("training-courses/", "")
    # Use just the final part if it has random suffixes
    if "-" in slug and len(slug.split("-")[-1]) == 5:
        # Has random suffix like "7ihjm", keep the meaningful part
        slug_parts = slug.rsplit("-", 1)
        if len(slug_parts[1]) == 5 and slug_parts[1].isalnum():
            slug = slug_parts[0]
    filepath = TRAINING_CONTENT_DIR / f"{slug}.md"

    shop_url = f"{ERPNEXT_URL}/shop/product/{slug}"

    # Get full description and convert HTML to clean text
    full_description = course.get("description") or course.get("short_description") or ""
    full_description = clean_html_to_markdown(full_description)

    # Fidelity check if file exists
    if filepath.exists():
        result = read_local_file(filepath)
        if result:
            local_frontmatter, local_content = result
            # Compare the description text content
            if check_fidelity(local_content, full_description):
                if not local_frontmatter.get('reviewedBy'):
                    if not dry_run:
                        local_frontmatter['reviewedBy'] = 'Automated Check'
                        local_frontmatter['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')
                        file_content = "---\n"
                        file_content += yaml.dump(local_frontmatter, default_flow_style=False, allow_unicode=True)
                        file_content += "---\n\n"
                        file_content += local_content.strip()
                        file_content += "\n"
                        filepath.write_text(file_content)
                print(f"  Unchanged (fidelity passed): {slug}")
                return filepath

    # For frontmatter description (SEO), truncate intelligently at sentence boundary
    short_desc_raw = course.get('short_description') or full_description or ''
    short_desc_raw = clean_html_to_markdown(short_desc_raw)
    short_desc = truncate_at_sentence(short_desc_raw, 200)

    # Use full description for the overview section
    description = full_description if full_description else "Course overview coming soon."

    # Escape quotes in description for YAML frontmatter
    short_desc_escaped = short_desc.replace('"', '\\"')

    price = course.get("price")
    price_currency = course.get("price_currency")
    price_line = ""
    if price is not None:
        price_line = f'\nprice: {price}'
        if price_currency:
            price_line += f'\nprice_currency: "{price_currency}"'

    content = f'''---
title: "{course.get('name', 'Training Course')}"
description: "{short_desc_escaped}"
thumbnail: "/img/training/{slug}.jpg"
item_code: "{course.get('item_code', '')}"
shop_url: "{shop_url}"{price_line}
tags:
  - Training
draft: false
reviewedBy: "Auto-generated"
reviewedDate: {datetime.now().strftime('%Y-%m-%d')}
---

{{{{< block
    title="{course.get('name', 'Training Course')}"
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
        print(f"  Would create: {slug}")
    else:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
        print(f"  Created: {slug}")

    return filepath


def save_calendar_data(sessions: list, dry_run: bool = False):
    """Save training sessions as JSON data for calendar view."""
    CALENDAR_DATA_DIR.mkdir(parents=True, exist_ok=True)
    data_file = CALENDAR_DATA_DIR / "events.json"

    calendar_events = []
    for session in sessions:
        calendar_events.append({
            "item_code": session["item_code"],
            "title": session.get("course_name", "Training"),
            "start": session.get("start_date", ""),
            "end": session.get("end_date", ""),
            "date_display": session.get("date_display", ""),
            "location": session.get("location", "Online"),
            "price": session.get("price"),
            "price_currency": session.get("price_currency"),
            "url": f"/training-courses/{session.get('course_slug', '')}/",
            "registration_url": session.get("shop_url", "/contact-us/"),
        })

    if dry_run:
        print(f"Would save {len(calendar_events)} sessions to: {data_file}")
    else:
        data_file.write_text(json.dumps(calendar_events, indent=2))
        print(f"Saved {len(calendar_events)} sessions to: {data_file}")

    return calendar_events


def list_training_content():
    """List all training content from ERPNext."""
    print("=" * 70)
    print("Training Content from ERPNext")
    print("=" * 70)

    print("\nFetching courses...")
    courses = fetch_training_courses()

    print(f"\nTraining Courses ({len(courses)}):")
    print("-" * 50)
    for course in courses:
        name = course.get("name", "Unknown")
        item_code = course.get("item_code", "")
        published = "✓" if course.get("published") else "✗"
        print(f"  {published} {name}")
        print(f"      Item: {item_code}")
        print(f"      Slug: {course.get('slug', '')}")

    print("\nFetching scheduled sessions...")
    sessions = fetch_all_scheduled_sessions()

    print(f"\nScheduled Sessions ({len(sessions)}):")
    print("-" * 50)
    if sessions:
        # Group by course
        by_course = {}
        for s in sessions:
            course_name = s.get("course_name", "Unknown")
            if course_name not in by_course:
                by_course[course_name] = []
            by_course[course_name].append(s)

        for course_name, course_sessions in by_course.items():
            print(f"\n  {course_name}:")
            for s in course_sessions:
                print(f"    • {s.get('date_display', 'TBD')} - {s.get('location', 'Online')}")
    else:
        print("  No scheduled sessions found")

    print("\nLocal Courses:")
    print("-" * 50)
    local = get_existing_courses()
    for slug in sorted(local.keys()):
        print(f"  - {slug}")

    print("\n" + "=" * 70)


def sync_training_content(dry_run: bool = False):
    """Sync training content from ERPNext."""
    print("=" * 70)
    print("Syncing Training Content from ERPNext")
    print("=" * 70)

    # Fetch and create course pages
    print("\nFetching courses...")
    courses = fetch_training_courses()
    local_courses = get_existing_courses()

    new_count = 0
    for course in courses:
        slug = course.get("slug") or slugify(course.get("name", ""))
        if slug and slug not in local_courses:
            create_course_page(course, dry_run)
            new_count += 1

    print(f"\nNew course pages: {new_count}")

    # Fetch and save scheduled sessions
    print("\nFetching scheduled sessions...")
    sessions = fetch_all_scheduled_sessions()
    if sessions:
        save_calendar_data(sessions, dry_run)
        print(f"Found {len(sessions)} scheduled sessions")
    else:
        print("No scheduled sessions found")
        if not dry_run:
            CALENDAR_DATA_DIR.mkdir(parents=True, exist_ok=True)
            events_file = CALENDAR_DATA_DIR / "events.json"
            events_file.write_text("[]")

    print("\n" + "=" * 70)
    print("Done!")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Fetch training content from ERPNext")
    parser.add_argument("--list", action="store_true", help="List content without syncing")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes")
    args = parser.parse_args()

    if args.list:
        list_training_content()
    else:
        sync_training_content(args.dry_run)


if __name__ == "__main__":
    main()
