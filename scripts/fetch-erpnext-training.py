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
from pathlib import Path
from datetime import datetime

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


def fetch_training_courses() -> list:
    """Fetch all training courses from ERPNext."""
    items = fetch_website_items()
    courses = []

    for item in items:
        # Filter for training-related items
        item_group = item.get("item_group", "").lower()
        if "training" not in item_group and "course" not in item_group:
            continue

        # Get full details
        details = fetch_website_item_details(item.get("name", ""))

        raw_slug = item.get("route", "").replace("shop/product/", "")
        # Clean up the slug
        clean_slug = raw_slug.replace("training/", "").replace("training-courses/", "")
        # Remove random suffixes if present
        if "-" in clean_slug:
            parts = clean_slug.rsplit("-", 1)
            if len(parts) > 1 and len(parts[1]) == 5 and parts[1].isalnum():
                clean_slug = parts[0]

        course = {
            "name": item.get("web_item_name") or item.get("item_name", ""),
            "item_code": item.get("item_code", ""),
            "slug": clean_slug,
            "raw_slug": raw_slug,  # Keep original for shop URL
            "short_description": item.get("short_description", ""),
            "description": details.get("web_long_description", ""),
            "published": item.get("published", 0),
        }

        # Extract additional fields from details
        if details:
            course["description"] = details.get("web_long_description", course["short_description"])

        courses.append(course)

    return courses


def fetch_all_scheduled_sessions() -> list:
    """Fetch all scheduled training sessions (variants) from ERPNext."""
    courses = fetch_training_courses()
    all_sessions = []

    for course in courses:
        item_code = course.get("item_code", "")
        if not item_code:
            continue

        variants = fetch_item_variants(item_code)
        if not variants:
            continue

        for attr in variants:
            display_date = attr.get("display_date", "")
            variant_code = attr.get("name", "")
            venue = attr.get("venue", "Online")
            if not display_date or not venue:
                continue

            start_date, end_date = parse_date_range(display_date)
            if not start_date:
                continue

            if start_date <= datetime.today().strftime("%Y-%m-%d"):
                continue

            all_sessions.append({
                "course_name": course.get("name", ""),
                "course_slug": course.get("slug", ""),
                "item_code": variant_code,
                "date_display": display_date,
                "start_date": start_date,
                "end_date": end_date,
                "location": venue.title() if venue else "Online",
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
    """Create a new training course page."""
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

    if filepath.exists():
        print(f"  Skipping (exists): {slug}")
        return filepath

    shop_url = f"{ERPNEXT_URL}/shop/product/{slug}"

    # Get full description and convert HTML to clean text
    full_description = course.get("description") or course.get("short_description") or ""
    full_description = clean_html_to_markdown(full_description)

    # For frontmatter description (SEO), truncate intelligently at sentence boundary
    short_desc_raw = course.get('short_description') or full_description or ''
    short_desc_raw = clean_html_to_markdown(short_desc_raw)
    short_desc = truncate_at_sentence(short_desc_raw, 200)

    # Use full description for the overview section
    description = full_description if full_description else "Course overview coming soon."

    # Escape quotes in description for YAML frontmatter
    short_desc_escaped = short_desc.replace('"', '\\"')

    content = f'''---
title: "{course.get('name', 'Training Course')}"
description: "{short_desc_escaped}"
thumbnail: "/img/training/{slug}.jpg"
item_code: "{course.get('item_code', '')}"
shop_url: "{shop_url}"
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
            "item_code": session.get("item_code", ""),
            "title": session.get("course_name", "Training"),
            "start": session.get("start_date", ""),
            "end": session.get("end_date", ""),
            "date_display": session.get("date_display", ""),
            "location": session.get("location", "Online"),
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
