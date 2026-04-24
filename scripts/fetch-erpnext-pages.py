#!/usr/bin/env python3
"""
Sync standalone pages from ERPNext to Hugo with fidelity checking.

Scrapes standalone pages (policies, resources, etc.) from the old Kartoza
website (ERPNext) and creates/updates Hugo content pages.

Features:
- Scrapes page content via web scraping (no API auth needed)
- Converts HTML to clean markdown
- Fidelity checking against existing local content
- Auto-marks pages as reviewed when content matches

Environment variables:
    ERPNEXT_URL: ERPNext instance URL (default: https://erp.kartoza.com)

Usage:
    ./fetch-erpnext-pages.py              # Full sync with fidelity checking
    ./fetch-erpnext-pages.py --dry-run    # Preview changes without writing
    ./fetch-erpnext-pages.py --list       # List pages that would be synced
    ./fetch-erpnext-pages.py --force      # Overwrite all pages
    ./fetch-erpnext-pages.py --verbose    # Verbose output
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
from tabulate import tabulate
import html2text

# Suppress XML parsing warning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Configuration
ERPNEXT_URL = os.environ.get('ERPNEXT_URL', 'https://erp.kartoza.com')

# Pages to sync: (old_path, content_dir_name, description)
# Each entry maps an old URL path to a Hugo content directory
PAGES_TO_SYNC = [
    ('/policies', 'policies', 'Policies index'),
    ('/privacy-policy', 'privacy-policy', 'Privacy Policy (POPI Act)'),
    ('/cancellation-policy', 'cancellation-policy', 'Cancellation Policy'),
    ('/conflict-of-interest-policy', 'conflict-of-interest-policy', 'Conflict of Interest Policy'),
    ('/child-protection-policy', 'child-protection-policy', 'Child Protection Policy'),
    ('/complaints-policy', 'complaints-policy', 'Data Protection Policy (GDPR)'),
    ('/anti-bribery-and-corruption-policy', 'anti-bribery-and-corruption-policy', 'Anti-Bribery and Corruption Policy'),
    ('/fraud-policy', 'fraud-policy', 'Fraud Prevention and Response Policy'),
    ('/code-of-conduct', 'code-of-conduct', 'Code of Conduct'),
    ('/coding-standards', 'coding-standards', 'Coding Standards'),
    ('/crowdfunding', 'crowdfunding', 'Crowdfunding'),
    ('/qgis-resources', 'qgis-resources', 'QGIS Resources'),
]


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


def check_fidelity(local_content: str, remote_content: str) -> bool:
    """Check if local and remote content match (ignoring formatting)."""
    local_norm = normalize_for_comparison(local_content)
    remote_norm = normalize_for_comparison(remote_content)
    return local_norm == remote_norm


def read_local_page(filepath: Path) -> tuple[dict, str] | None:
    """Read a local Hugo page file and extract front matter and content."""
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


def fetch_page(url_path: str, verbose: bool = False) -> dict | None:
    """
    Fetch a page from ERPNext by scraping the public URL.

    Returns dict with 'title', 'description', 'content' keys.
    """
    url = f"{ERPNEXT_URL}{url_path}"

    if verbose:
        print(f"  Fetching: {url}", file=sys.stderr)

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  Error fetching '{url_path}': {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title
    def get_meta(attr_name, attr_value):
        tag = soup.find('meta', attrs={attr_name: attr_value})
        return tag.get('content', '') if tag else ''

    title = get_meta('property', 'og:title') or get_meta('name', 'title')
    if not title:
        h1 = soup.find('h1')
        title = h1.get_text(strip=True) if h1 else ''
    if not title:
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else 'Untitled'
    # Clean title prefix
    title = re.sub(r'^Kartoza\s*[-|]\s*', '', title)

    # Extract description
    description = get_meta('name', 'description') or get_meta('property', 'og:description') or ''

    # Extract main content
    # Try common ERPNext page content containers
    content_el = (
        soup.find('div', class_='wiki-content')
        or soup.find('div', class_='web-page-content')
        or soup.find('div', attrs={'itemprop': 'articleBody'})
        or soup.find('article')
        or soup.find('main')
    )

    if not content_el:
        # Fallback: find the main content area
        # ERPNext pages often use .page-content or .main-section
        content_el = (
            soup.find('div', class_='page-content')
            or soup.find('div', class_='main-section')
            or soup.find('div', class_='container', attrs={'data-page-container': True})
        )

    if not content_el:
        # Last resort: get all content from body, stripping nav/header/footer
        content_el = soup.find('body')
        if content_el:
            for tag in content_el.find_all(['nav', 'header', 'footer', 'script', 'style']):
                tag.decompose()

    content_html = str(content_el) if content_el else ''

    return {
        'title': title.strip(),
        'description': description.strip()[:200],
        'content_html': content_html,
        'url_path': url_path,
    }


def html_to_markdown(html_content: str) -> str:
    """Convert HTML content to clean markdown using html2text."""
    if not html_content:
        return ''

    h = html2text.HTML2Text()
    h.body_width = 0  # Don't wrap lines
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.skip_internal_links = False
    h.inline_links = True
    h.protect_links = True
    h.unicode_snob = True

    markdown = h.handle(html_content)

    # Clean up: remove excessive blank lines
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)

    return markdown.strip()


def sync_page(page_data: dict, content_dir: Path, dir_name: str,
              dry_run: bool = False, force: bool = False,
              verbose: bool = False) -> dict:
    """
    Sync a single page from ERPNext to Hugo.

    Returns dict with 'status' and 'fidelity' keys.
    """
    page_dir = content_dir / dir_name
    filepath = page_dir / 'index.md'

    remote_content = html_to_markdown(page_data['content_html'])

    if filepath.exists() and not force:
        result = read_local_page(filepath)
        if result:
            local_frontmatter, local_content = result
            if check_fidelity(local_content, remote_content):
                # Content matches
                if not local_frontmatter.get('reviewedBy'):
                    if not dry_run:
                        local_frontmatter['reviewedBy'] = 'Automated Check'
                        local_frontmatter['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')
                        _write_page(filepath, local_frontmatter, local_content.strip())
                return {'status': 'unchanged', 'fidelity': 'passed', 'file': str(filepath.relative_to(content_dir))}

        status = 'updated'
    elif filepath.exists() and force:
        status = 'forced'
    else:
        status = 'new'

    # Build front matter
    front_matter = {
        'title': page_data['title'],
        'description': page_data['description'],
        'type': 'page',
        'layout': 'single',
        'reviewedBy': 'Automated Check',
        'reviewedDate': datetime.now().strftime('%Y-%m-%d'),
        'erpnext_path': page_data['url_path'],
    }

    if not dry_run:
        page_dir.mkdir(parents=True, exist_ok=True)
        _write_page(filepath, front_matter, remote_content)

    return {'status': status, 'fidelity': 'auto-reviewed', 'file': str(filepath.relative_to(content_dir))}


def _write_page(filepath: Path, front_matter: dict, content: str) -> None:
    """Write a Hugo page file with front matter and content."""
    file_content = "---\n"
    file_content += yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
    file_content += "---\n\n"
    file_content += content.strip()
    file_content += "\n"

    filepath.write_text(file_content)


def print_status_table(results: list[dict], dry_run: bool = False) -> None:
    """Print a rich status table of sync results."""
    if not results:
        print("\nNo pages found.", file=sys.stderr)
        return

    table_data = []
    for r in results:
        title = r['title'][:40] + ('...' if len(r['title']) > 40 else '')
        fidelity = r.get('fidelity', '-')

        if fidelity == 'auto-reviewed':
            fidelity_str = 'auto-reviewed'
        elif fidelity == 'passed':
            fidelity_str = 'passed'
        elif fidelity == 'failed':
            fidelity_str = 'failed'
        else:
            fidelity_str = fidelity

        table_data.append([
            title,
            r.get('path', '-'),
            r['status'],
            fidelity_str
        ])

    header = "ERPNEXT PAGE SYNC REPORT"
    if dry_run:
        header += " (DRY RUN)"

    print("\n" + "=" * 80, file=sys.stderr)
    print(f"  {header}", file=sys.stderr)
    print(f"  Source: {ERPNEXT_URL} | Date: {datetime.now().strftime('%Y-%m-%d')}", file=sys.stderr)
    print("=" * 80, file=sys.stderr)

    headers = ['Title', 'Path', 'Status', 'Fidelity']
    print(tabulate(table_data, headers=headers, tablefmt='simple'), file=sys.stderr)

    print("-" * 80, file=sys.stderr)
    new_count = sum(1 for r in results if r['status'] == 'new')
    unchanged_count = sum(1 for r in results if r['status'] == 'unchanged')
    updated_count = sum(1 for r in results if r['status'] == 'updated')
    error_count = sum(1 for r in results if r['status'] == 'error')

    print(f"  Summary: {len(results)} total | {new_count} new | {unchanged_count} unchanged | {updated_count} updated | {error_count} errors", file=sys.stderr)
    print("=" * 80, file=sys.stderr)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Sync standalone pages from ERPNext with fidelity checking'
    )
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show what would happen without writing files')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Force overwrite all files, ignoring fidelity check')
    parser.add_argument('--list', '-l', action='store_true',
                        help='Only list pages that would be synced')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show verbose output')
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    content_dir = script_dir.parent / 'content'

    if not content_dir.exists():
        print(f"Error: Content directory not found: {content_dir}", file=sys.stderr)
        sys.exit(2)

    if args.list:
        results = []
        for url_path, dir_name, description in PAGES_TO_SYNC:
            filepath = content_dir / dir_name / 'index.md'
            exists = filepath.exists()
            results.append({
                'title': description,
                'path': url_path,
                'status': 'exists' if exists else 'missing',
                'fidelity': '-'
            })
        print_status_table(results, dry_run=True)
        return

    print(f"Syncing {len(PAGES_TO_SYNC)} standalone pages from {ERPNEXT_URL}...", file=sys.stderr)

    results = []
    errors_occurred = False

    for url_path, dir_name, description in PAGES_TO_SYNC:
        if args.verbose:
            print(f"Processing: {description} ({url_path})", file=sys.stderr)

        page_data = fetch_page(url_path, verbose=args.verbose)
        if not page_data:
            results.append({
                'title': description,
                'path': url_path,
                'status': 'error',
                'fidelity': '-'
            })
            errors_occurred = True
            continue

        sync_result = sync_page(
            page_data, content_dir, dir_name,
            dry_run=args.dry_run, force=args.force, verbose=args.verbose
        )

        results.append({
            'title': page_data.get('title', description),
            'path': url_path,
            'status': sync_result['status'],
            'fidelity': sync_result['fidelity'],
            'file': sync_result.get('file', '')
        })

    print_status_table(results, dry_run=args.dry_run)

    if errors_occurred:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
