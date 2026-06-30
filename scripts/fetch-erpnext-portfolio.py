#!/usr/bin/env python3
"""Fetch portfolio/project articles from ERPNext and create Hugo content files.

Only fetches new articles that don't exist locally to preserve local edits.

Environment variables:
    ERPNEXT_URL: ERPNext instance URL (default: https://erp.kartoza.com)
    ERPNEXT_API_KEY / GATEWAY_ERPNEXT_API_KEY: API key for authentication
    ERPNEXT_API_SECRET / GATEWAY_ERPNEXT_API_SECRET: API secret for authentication

Usage:
    ./fetch-erpnext-portfolio.py [--dry-run] [--force] [--list]
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import warnings

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import yaml
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from dateutil import parser as date_parser
from tabulate import tabulate
import html2text

warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _load_env_file(path: Path) -> bool:
    """Load KEY=VALUE entries from a dotenv-like file into os.environ.

    :param path: Path to the env file to load.
    :type path: Path

    :returns: True if the file was found and read, False otherwise.
    :rtype: bool
    """
    if not path.exists():
        return False

    try:
        lines = path.read_text().splitlines()
    except (IOError, OSError):
        return False

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()

        if key.startswith('export '):
            key = key[len('export '):].strip()

        if (
            (value.startswith('"') and value.endswith('"'))
            or (value.startswith("'") and value.endswith("'"))
        ):
            value = value[1:-1]

        if key and key not in os.environ:
            os.environ[key] = value

    return True


def _load_default_env_files() -> list[Path]:
    """Load common environment files used by this repository.

    :returns: List of env file paths that were successfully loaded.
    :rtype: list[Path]
    """
    loaded_files: list[Path] = []
    candidates = [
        PROJECT_ROOT / '.env',
        PROJECT_ROOT / 'deployment' / '.env',
    ]
    for path in candidates:
        if _load_env_file(path):
            loaded_files.append(path)
    return loaded_files


LOADED_ENV_FILES = _load_default_env_files()


def _normalize_erpnext_base_url(url: str) -> str:
    """Normalize ERPNext URL to a base URL without trailing /api.

    :param url: Raw URL string to normalize.
    :type url: str

    :returns: Normalized base URL.
    :rtype: str
    """
    normalized = url.strip().rstrip('/')
    if normalized.endswith('/api'):
        return normalized[:-4]
    return normalized


def _get_erpnext_config() -> tuple[str, str, str]:
    """Resolve ERPNext URL and credentials from environment.

    Supports legacy and gateway-prefixed variable names.

    :returns: Tuple of (base_url, api_key, api_secret).
    :rtype: (str, str, str)
    """
    raw_url = os.environ.get('ERPNEXT_URL', 'https://erp.kartoza.com')
    api_key = (
        os.environ.get('ERPNEXT_API_KEY')
        or os.environ.get('GATEWAY_ERPNEXT_API_KEY')
        or ''
    )
    api_secret = (
        os.environ.get('ERPNEXT_API_SECRET')
        or os.environ.get('GATEWAY_ERPNEXT_API_SECRET')
        or ''
    )
    return _normalize_erpnext_base_url(raw_url), api_key, api_secret


ERPNEXT_URL, API_KEY, API_SECRET = _get_erpnext_config()

PORTFOLIO_DOCTYPE = os.environ.get('ERPNEXT_PORTFOLIO_DOCTYPE', 'Portfolio')
CONTENT_DIR = PROJECT_ROOT / 'content' / 'portfolio'


def _build_http_session() -> requests.Session:
    """Create an HTTP session with retries for transient network failures.

    :returns: Configured requests Session.
    :rtype: requests.Session
    """
    session = requests.Session()

    retry = Retry(
        total=5,
        connect=5,
        read=5,
        status=5,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(['GET']),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    session.headers.update({
        'Accept': 'application/json',
        'User-Agent': 'kartoza-website-sync/1.0',
    })

    if API_KEY and API_SECRET:
        session.headers.update(
            {'Authorization': f'token {API_KEY}:{API_SECRET}'}
        )

    return session


HTTP_SESSION = _build_http_session()


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug.

    :param text: Text to slugify.
    :type text: str

    :returns: Slugified string.
    :rtype: str
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def normalize_for_comparison(content: str) -> str:
    """Normalize content for fidelity comparison, focusing on text only.

    :param content: Raw content string (may contain HTML or shortcodes).
    :type content: str

    :returns: Normalized, lowercase, whitespace-collapsed plain text.
    :rtype: str
    """
    if not content:
        return ''

    content = re.sub(r'\{\{[<>%].*?[>%]\}\}', '', content)

    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text(separator=' ')

    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()


def check_fidelity(local_content: str, erpnext_content: str) -> bool:
    """Check if local and ERPNext content match, ignoring formatting.

    :param local_content: Local Hugo markdown content.
    :type local_content: str

    :param erpnext_content: ERPNext content to compare against.
    :type erpnext_content: str

    :returns: True if text content matches.
    :rtype: bool
    """
    return (
        normalize_for_comparison(local_content)
        == normalize_for_comparison(erpnext_content)
    )


def html_to_markdown(html_content: str) -> str:
    """Convert HTML content to clean markdown.

    :param html_content: HTML string to convert.
    :type html_content: str

    :returns: Cleaned markdown string.
    :rtype: str
    """
    if not html_content:
        return ''

    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.unicode_snob = True
    converter.protect_links = True
    converter.wrap_links = False
    converter.mark_code = True

    markdown = converter.handle(html_content)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    return markdown.strip()


def read_local_file(filepath: Path) -> tuple[dict, str] | None:
    """Read a local Hugo file and extract front matter and content.

    :param filepath: Path to the Hugo markdown file.
    :type filepath: Path

    :returns: Tuple of (front_matter_dict, content_str) or None.
    :rtype: (dict, str) or None
    """
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


def find_local_file(
    content_dir: Path, erpnext_id: str, title: str
) -> Path | None:
    """Find a local Hugo file matching the ERPNext portfolio item.

    Matches by erpnext_id in front matter first, then by slugified title.

    :param content_dir: Directory containing Hugo markdown files.
    :type content_dir: Path

    :param erpnext_id: ERPNext document name to match.
    :type erpnext_id: str

    :param title: Portfolio item title for slug-based fallback.
    :type title: str

    :returns: Path to matching file or None.
    :rtype: Path or None
    """
    for filepath in content_dir.glob('*.md'):
        if filepath.name in ('_index.md', 'index.md'):
            continue
        result = read_local_file(filepath)
        if result:
            front_matter, _ = result
            if front_matter.get('erpnext_id') == erpnext_id:
                return filepath

    expected_path = content_dir / f'{slugify(title)}.md'
    if expected_path.exists():
        return expected_path

    return None


def fetch_portfolio_list() -> list[dict]:
    """Fetch list of published portfolio items from ERPNext.

    :returns: List of portfolio item summary dicts.
    :rtype: list[dict]
    """
    fields = [
        'name', 'title', 'client', 'publish', 'modified', 'creation',
    ]
    filters = [['publish', '=', 1]]

    url = f'{ERPNEXT_URL}/api/resource/{PORTFOLIO_DOCTYPE}'
    params = {
        'fields': json.dumps(fields),
        'filters': json.dumps(filters),
        'limit_page_length': 0,
    }

    try:
        response = HTTP_SESSION.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except requests.HTTPError as exc:
        status_code = (
            exc.response.status_code if exc.response is not None else None
        )
        if status_code in (401, 403):
            print(
                f'Authentication/permission error fetching portfolio list '
                f'(HTTP {status_code}). '
                'Set ERPNEXT_API_KEY/ERPNEXT_API_SECRET '
                '(or GATEWAY_* variants).',
                file=sys.stderr,
            )
            return []
        print(
            f'Error fetching portfolio list (HTTP {status_code}): {exc}',
            file=sys.stderr,
        )
        return []
    except requests.RequestException as exc:
        print(f'Error fetching portfolio list: {exc}', file=sys.stderr)
        return []


def fetch_portfolio_detail(name: str) -> dict | None:
    """Fetch full portfolio item details from ERPNext.

    :param name: ERPNext document name.
    :type name: str

    :returns: Portfolio item data dict or None on failure.
    :rtype: dict or None
    """
    url = f'{ERPNEXT_URL}/api/resource/{PORTFOLIO_DOCTYPE}/{name}'

    try:
        response = HTTP_SESSION.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('data', {})
    except requests.RequestException as exc:
        print(
            f'Error fetching portfolio detail for {name}: {exc}',
            file=sys.stderr,
        )
        return None


def _resolve_thumbnail(item: dict) -> str:
    """Return the best available thumbnail URL for a Portfolio item.

    Prefers the first image from the images child table, falling back to the
    placeholder when none are present.

    :param item: Portfolio item data from ERPNext.
    :type item: dict

    :returns: Absolute or root-relative image URL.
    :rtype: str
    """
    images = item.get('images') or []
    for img in images:
        website_image = img.get('website_image', '').strip()
        if website_image:
            if website_image.startswith('/files/'):
                return f'{ERPNEXT_URL}{website_image}'
            return website_image
    return '/img/portfolio/placeholder.png'


def portfolio_to_hugo_frontmatter(
    item: dict, mark_reviewed: bool = False
) -> dict:
    """Convert an ERPNext Portfolio item to Hugo front matter.

    :param item: Portfolio item data from ERPNext.
    :type item: dict

    :param mark_reviewed: If True, add reviewedBy/reviewedDate fields.
    :type mark_reviewed: bool

    :returns: Front matter dictionary for Hugo.
    :rtype: dict
    """
    creation_date = item.get('creation')
    if creation_date:
        try:
            date_str = date_parser.parse(
                str(creation_date)
            ).strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            date_str = datetime.now().strftime('%Y-%m-%d')
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')

    title = item.get('title') or item.get('name', 'Untitled')
    subject = item.get('subject', '')

    services = [
        s.get('service', '')
        for s in (item.get('services_listed') or [])
        if s.get('service')
    ]
    technologies = [
        t.get('technology', '')
        for t in (item.get('technologies') or [])
        if t.get('technology')
    ]

    tags = ['Project']

    front_matter = {
        'title': title,
        'description': subject[:200] if subject else f'Project: {title}',
        'thumbnail': _resolve_thumbnail(item),
        'tags': tags,
        'client': item.get('client', ''),
        'date': date_str,
        'services': services,
        'technologies': technologies,
        'github': item.get('github_page', ''),
        'erpnext_id': item.get('name', ''),
        'erpnext_modified': item.get('modified', ''),
    }

    if mark_reviewed:
        front_matter['reviewedBy'] = 'Automated Check'
        front_matter['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')

    return front_matter


def portfolio_to_hugo_content(item: dict) -> str:
    """Convert ERPNext Portfolio content to Hugo markdown.

    :param item: Portfolio item data from ERPNext.
    :type item: dict

    :returns: Hugo markdown content string.
    :rtype: str
    """
    title = item.get('title') or item.get('name', 'Project')
    client = item.get('client', '')
    subject = item.get('subject', '')
    body = item.get('body', '')

    body_markdown = html_to_markdown(body) if body else ''
    safe_title = title.replace('"', '\\"')
    intro = subject or body_markdown[:200] or 'Project description.'

    content = (
        f'{{{{< block\n'
        f'    title="{safe_title}"\n'
        f'    subtitle="Project"\n'
        f'    class="is-primary"\n'
        f'    sub-block-side="bottom"\n'
        f'>}}}}\n'
        f'{intro}\n'
        f'{{{{< /block >}}}}\n\n'
        f'## Overview\n\n'
        f'{body_markdown if body_markdown else subject or "Project overview and details."}\n'
    )

    if client:
        content += f'\n## Client\n\n{client}\n'

    technologies = [
        t.get('technology', '')
        for t in (item.get('technologies') or [])
        if t.get('technology')
    ]
    if technologies:
        content += f'\n## Technologies\n\n'
        content += '\n'.join(f'- {t}' for t in technologies)
        content += '\n'

    github = item.get('github_page', '')
    if github:
        content += f'\n## Source Code\n\n[GitHub]({github})\n'

    return content.strip()


def _update_review_fields(
    filepath: Path, front_matter: dict, content: str
) -> None:
    """Update review fields in an existing Hugo file.

    :param filepath: Path to the file to update.
    :type filepath: Path

    :param front_matter: Existing front matter dict.
    :type front_matter: dict

    :param content: Existing body content string.
    :type content: str
    """
    front_matter['reviewedBy'] = 'Automated Check'
    front_matter['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')

    file_content = '---\n'
    file_content += yaml.dump(
        front_matter, default_flow_style=False, allow_unicode=True
    )
    file_content += '---\n\n'
    file_content += content.strip()
    file_content += '\n'

    filepath.write_text(file_content)


def sync_portfolio_item(
    item: dict,
    content_dir: Path,
    dry_run: bool = False,
    force: bool = False,
    verbose: bool = False,
) -> dict:
    """Sync a single portfolio item from ERPNext to Hugo.

    Performs fidelity checking and updates review fields when content matches.

    :param item: Portfolio item data from ERPNext.
    :type item: dict

    :param content_dir: Hugo content directory for portfolio files.
    :type content_dir: Path

    :param dry_run: If True, do not write any files.
    :type dry_run: bool

    :param force: If True, overwrite existing files regardless of fidelity.
    :type force: bool

    :param verbose: If True, print detailed per-item output.
    :type verbose: bool

    :returns: Result dict with 'title', 'client', 'status', 'fidelity', 'file'.
    :rtype: dict
    """
    erpnext_id = item.get('name', '')
    title = item.get('title') or item.get('name', 'Untitled')
    client = item.get('client', '')
    erpnext_content = portfolio_to_hugo_content(item)

    local_file = find_local_file(content_dir, erpnext_id, title)

    if local_file and not force:
        result = read_local_file(local_file)
        if result:
            local_frontmatter, local_content = result
            if check_fidelity(local_content, erpnext_content):
                if not local_frontmatter.get('reviewedBy') and not dry_run:
                    _update_review_fields(
                        local_file, local_frontmatter, local_content
                    )
                return {
                    'title': title,
                    'client': client,
                    'status': 'unchanged',
                    'fidelity': 'passed',
                    'file': local_file.name,
                }
        status = 'updated'
        filepath = local_file
    elif local_file and force:
        status = 'forced'
        filepath = local_file
    else:
        status = 'new'
        filepath = content_dir / f'{slugify(title)}.md'

    front_matter = portfolio_to_hugo_frontmatter(item, mark_reviewed=True)

    file_content = '---\n'
    file_content += yaml.dump(
        front_matter, default_flow_style=False, allow_unicode=True
    )
    file_content += '---\n\n'
    file_content += erpnext_content
    file_content += '\n'

    if verbose:
        print(f'  {status.capitalize()}: {filepath.name}', file=sys.stderr)

    if not dry_run:
        content_dir.mkdir(parents=True, exist_ok=True)
        filepath.write_text(file_content)

    return {
        'title': title,
        'client': client,
        'status': status,
        'fidelity': 'auto-reviewed',
        'file': filepath.name,
    }


def print_results_table(results: list[dict], dry_run: bool = False) -> None:
    """Print a formatted results table to stderr.

    :param results: List of result dicts from sync operations.
    :type results: list[dict]

    :param dry_run: If True, include DRY RUN label in header.
    :type dry_run: bool
    """
    if not results:
        print('\nNo portfolio items found.', file=sys.stderr)
        return

    header = 'ERPNEXT PORTFOLIO FETCH'
    if dry_run:
        header += ' (DRY RUN)'

    print(f'\n{"=" * 80}', file=sys.stderr)
    print(f'  {header}', file=sys.stderr)
    print(
        f'  Source: {ERPNEXT_URL} | Date: {datetime.now().strftime("%Y-%m-%d")}',
        file=sys.stderr,
    )
    print(f'{"=" * 80}', file=sys.stderr)

    table_data = []
    for result in results:
        fidelity = result.get('fidelity', '-')
        if fidelity == 'auto-reviewed':
            fidelity_str = '✓ auto-reviewed'
        elif fidelity == 'passed':
            fidelity_str = '✓ passed'
        else:
            fidelity_str = fidelity

        table_data.append([
            result['title'][:40] + ('...' if len(result['title']) > 40 else ''),
            result.get('client', '-')[:20],
            result['status'],
            fidelity_str,
            result.get('file', '-'),
        ])

    headers = ['Project', 'Client', 'Status', 'Fidelity', 'File']
    print(tabulate(table_data, headers=headers, tablefmt='simple'), file=sys.stderr)

    new_count = sum(1 for r in results if r['status'] == 'new')
    updated_count = sum(1 for r in results if r['status'] == 'updated')
    unchanged_count = sum(1 for r in results if r['status'] == 'unchanged')
    error_count = sum(1 for r in results if r['status'] == 'error')

    print(f'\n{"=" * 80}', file=sys.stderr)
    print(
        f'  Total: {len(results)} | New: {new_count} | '
        f'Updated: {updated_count} | Unchanged: {unchanged_count} | '
        f'Errors: {error_count}',
        file=sys.stderr,
    )
    print(f'{"=" * 80}', file=sys.stderr)


def main() -> int:
    """Main entry point.

    :returns: Exit code (0 on success, 1 on errors).
    :rtype: int
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='Fetch portfolio items from ERPNext with fidelity checking'
    )
    parser.add_argument(
        '--dry-run', '-n', action='store_true',
        help='Show what would be fetched without creating files',
    )
    parser.add_argument(
        '--force', '-f', action='store_true',
        help='Overwrite existing files regardless of fidelity',
    )
    parser.add_argument(
        '--list', '-l', action='store_true',
        help='Only list available items, do not fetch',
    )
    parser.add_argument(
        '--doctype', '-d', type=str, default=PORTFOLIO_DOCTYPE,
        help=f'ERPNext doctype to fetch (default: {PORTFOLIO_DOCTYPE})',
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Show detailed per-item output',
    )
    args = parser.parse_args()

    if args.doctype != PORTFOLIO_DOCTYPE:
        globals()['PORTFOLIO_DOCTYPE'] = args.doctype

    if not API_KEY or not API_SECRET:
        print(
            'Warning: API credentials not set; attempting unauthenticated access. '
            'Private ERPNext endpoints may return HTTP 401/403.',
            file=sys.stderr,
        )
        print(
            'Looked in current shell plus .env files at '
            f'{PROJECT_ROOT / ".env"} and {PROJECT_ROOT / "deployment" / ".env"}.',
            file=sys.stderr,
        )
        print(file=sys.stderr)

    if not CONTENT_DIR.exists():
        print(
            f'Error: Content directory not found: {CONTENT_DIR}',
            file=sys.stderr,
        )
        return 1

    print(f'Fetching portfolio list from {ERPNEXT_URL}...', file=sys.stderr)
    print(f'Using doctype: {PORTFOLIO_DOCTYPE}', file=sys.stderr)

    items = fetch_portfolio_list()

    if not items:
        print('No portfolio items found or error occurred.', file=sys.stderr)
        return 1

    print(f'Found {len(items)} portfolio item(s)', file=sys.stderr)

    if args.list:
        table_data = [
            [
                item.get('title') or item.get('name', 'Untitled'),
                item.get('client', '-'),
                'Published',
                item.get('name', '-'),
            ]
            for item in items
        ]
        headers = ['Project', 'Client', 'Status', 'ERPNext ID']
        print(file=sys.stderr)
        print(
            tabulate(table_data, headers=headers, tablefmt='simple'),
            file=sys.stderr,
        )
        return 0

    if args.dry_run:
        print('DRY RUN - no files will be written', file=sys.stderr)
    print(file=sys.stderr)

    results = []
    errors_occurred = False

    for item_summary in items:
        item_name = item_summary.get('name')
        if not item_name:
            continue

        if args.verbose:
            title = item_summary.get('title') or item_name
            print(f'Fetching: {title}', file=sys.stderr)

        item = fetch_portfolio_detail(item_name)
        if not item:
            results.append({
                'title': item_summary.get('title', 'Unknown'),
                'client': item_summary.get('client', '-'),
                'status': 'error',
                'fidelity': '-',
                'file': '-',
            })
            errors_occurred = True
            continue

        result = sync_portfolio_item(
            item,
            CONTENT_DIR,
            dry_run=args.dry_run,
            force=args.force,
            verbose=args.verbose,
        )
        results.append(result)

    print_results_table(results, dry_run=args.dry_run)

    return 1 if errors_occurred else 0


if __name__ == '__main__':
    sys.exit(main())
