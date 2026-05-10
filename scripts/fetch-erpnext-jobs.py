#!/usr/bin/env python3
"""
Sync job opportunities from ERPNext to Hugo with fidelity checking.

Fetches published Job Opening records from ERPNext and creates/updates
Hugo content pages in content/careers/.

Features:
- Fetches job openings from ERPNext Job Opening doctype
- Converts HTML descriptions to clean markdown
- Fidelity checking against existing local content
- Auto-marks jobs as reviewed when content matches
- Publishes/unpublishes based on ERPNext status
- Preserves tags and metadata

Environment variables:
    ERPNEXT_URL: ERPNext instance URL (default: https://erp.kartoza.com)

Usage:
    ./fetch-erpnext-jobs.py              # Full sync with fidelity checking
    ./fetch-erpnext-jobs.py --dry-run    # Preview changes without writing
    ./fetch-erpnext-jobs.py --list       # List available job openings
    ./fetch-erpnext-jobs.py --force      # Overwrite all files
    ./fetch-erpnext-jobs.py --verbose    # Verbose output
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
CONTENT_DIR = Path(__file__).parent.parent / 'content' / 'careers'


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


def read_local_file(filepath: Path) -> tuple[dict, str] | None:
    """
    Read a local Hugo file and extract front matter and content.

    Returns:
        Tuple of (front_matter_dict, content_str) or None if file doesn't exist
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


def find_local_file(content_dir: Path, erpnext_id: str, title: str) -> Path | None:
    """
    Find a local Hugo file matching the ERPNext job opening.

    Matches by:
    1. erpnext_id in front matter (primary)
    2. Slugified title matching filename (fallback)
    """
    for filepath in content_dir.glob('*.md'):
        if filepath.name == '_index.md' or filepath.name == 'index.md':
            continue
        result = read_local_file(filepath)
        if result:
            front_matter, _ = result
            if front_matter.get('erpnext_id') == erpnext_id:
                return filepath

    expected_filename = f"{slugify(title)}.md"
    expected_path = content_dir / expected_filename
    if expected_path.exists():
        return expected_path

    return None


def fetch_job_openings() -> list:
    """Fetch job openings from ERPNext API."""
    fields = [
        'name', 'job_title', 'status', 'description',
        'designation', 'department', 'location',
        'publish', 'route', 'creation', 'modified',
    ]
    filters = []

    url = f"{ERPNEXT_URL}/api/resource/Job Opening"
    params = {
        'fields': str(fields),
        'filters': str(filters),
        'limit_page_length': 100,
        'order_by': 'creation desc',
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('data', [])
    except requests.RequestException as e:
        print(f"Error fetching job openings: {e}")
        return []


def fetch_job_detail(job_name: str) -> dict | None:
    """Fetch full job opening details from ERPNext API."""
    url = f"{ERPNEXT_URL}/api/resource/Job Opening/{job_name}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get('data', {})
    except requests.RequestException as e:
        print(f"Error fetching job detail for {job_name}: {e}")
        return None


def html_to_markdown(html_content: str) -> str:
    """Convert HTML content to clean markdown."""
    if not html_content:
        return ''

    h = html2text.HTML2Text()
    h.body_width = 0  # No wrapping
    h.unicode_snob = True
    h.protect_links = True
    h.wrap_links = False
    h.mark_code = True

    md = h.handle(html_content)

    # Clean up excessive blank lines
    md = re.sub(r'\n{3,}', '\n\n', md)

    return md.strip()


def job_to_hugo_frontmatter(job: dict, mark_reviewed: bool = False) -> dict:
    """Convert ERPNext job opening data to Hugo front matter."""
    front_matter = {
        'title': job.get('job_title', 'Untitled Position'),
        'erpnext_id': job.get('name', ''),
        'type': 'careers',
        'layout': 'single',
    }

    # Status / draft
    status = job.get('status', 'Open')
    published = job.get('publish', 0)
    if status == 'Closed' or not published:
        front_matter['draft'] = True

    # Date fields
    creation = job.get('creation')
    if creation:
        try:
            dt = datetime.fromisoformat(str(creation).replace('Z', '+00:00'))
            front_matter['date'] = dt.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        except (ValueError, TypeError):
            front_matter['date'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')

    modified = job.get('modified')
    if modified:
        try:
            dt = datetime.fromisoformat(str(modified).replace('Z', '+00:00'))
            front_matter['lastmod'] = dt.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        except (ValueError, TypeError):
            pass

    # Tags from department, designation, location
    tags = ['Career']
    if job.get('designation'):
        tags.append(job['designation'])
    if job.get('department'):
        tags.append(job['department'])
    if job.get('location'):
        tags.append(job['location'])
    front_matter['tags'] = tags

    # Extra metadata
    if job.get('designation'):
        front_matter['designation'] = job['designation']
    if job.get('department'):
        front_matter['department'] = job['department']
    if job.get('location'):
        front_matter['location'] = job['location']
    if job.get('status'):
        front_matter['job_status'] = job['status']

    # Review fields
    if mark_reviewed:
        front_matter['reviewedBy'] = 'Automated Check'
        front_matter['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')

    return front_matter


def sync_job(job: dict, content_dir: Path, dry_run: bool = False,
             force: bool = False, verbose: bool = False) -> dict:
    """
    Sync a single job opening from ERPNext to Hugo.

    Performs fidelity checking and updates review fields.
    """
    erpnext_id = job.get('name', '')
    title = job.get('job_title', 'Untitled')
    erpnext_content = job.get('description', '')

    # Find existing local file
    local_file = find_local_file(content_dir, erpnext_id, title)

    if local_file and not force:
        result = read_local_file(local_file)
        if result:
            local_frontmatter, local_content = result
            if check_fidelity(local_content, erpnext_content):
                # Content matches - fidelity passed
                if not local_frontmatter.get('reviewedBy'):
                    if not dry_run:
                        _update_review_fields(local_file, local_frontmatter, local_content)
                return {'status': 'unchanged', 'fidelity': 'passed', 'file': local_file.name,
                        'title': title}

        status = 'updated'
        filepath = local_file
    elif local_file and force:
        status = 'forced'
        filepath = local_file
    else:
        status = 'new'
        slug = slugify(title)
        filepath = content_dir / f"{slug}.md"

    # Generate content
    front_matter = job_to_hugo_frontmatter(job, mark_reviewed=True)
    content = html_to_markdown(erpnext_content)

    # Build file content
    file_content = "---\n"
    file_content += yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
    file_content += "---\n\n"
    file_content += content
    file_content += "\n"

    if not dry_run:
        content_dir.mkdir(parents=True, exist_ok=True)
        filepath.write_text(file_content)

    return {'status': status, 'fidelity': 'auto-reviewed', 'file': filepath.name,
            'title': title}


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


def unpublish_closed_jobs(jobs: list, content_dir: Path, dry_run: bool = False,
                          verbose: bool = False) -> list:
    """
    Mark local job files as draft if the corresponding ERPNext job is closed or unpublished.

    Returns list of result dicts for unpublished jobs.
    """
    results = []
    erpnext_ids = {j.get('name') for j in jobs}
    open_ids = {j.get('name') for j in jobs
                if j.get('status') == 'Open' and j.get('publish', 0)}

    for filepath in content_dir.glob('*.md'):
        if filepath.name in ('_index.md', 'index.md'):
            continue

        result = read_local_file(filepath)
        if not result:
            continue

        front_matter, content = result
        erpnext_id = front_matter.get('erpnext_id')
        if not erpnext_id:
            continue

        # If the job exists in ERPNext but is closed/unpublished, mark as draft
        if erpnext_id in erpnext_ids and erpnext_id not in open_ids:
            if not front_matter.get('draft'):
                front_matter['draft'] = True
                front_matter['job_status'] = 'Closed'
                if not dry_run:
                    _update_review_fields(filepath, front_matter, content)
                results.append({
                    'status': 'unpublished',
                    'fidelity': '-',
                    'file': filepath.name,
                    'title': front_matter.get('title', filepath.stem),
                })
                if verbose:
                    print(f"  Unpublished: {filepath.name}")

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Sync job opportunities from ERPNext with fidelity checking'
    )
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview changes without writing files')
    parser.add_argument('--list', action='store_true',
                        help='List job openings from ERPNext')
    parser.add_argument('--force', action='store_true',
                        help='Force overwrite all files')
    parser.add_argument('--verbose', action='store_true',
                        help='Show detailed output')

    args = parser.parse_args()

    print(f"Fetching job openings from {ERPNEXT_URL}...")
    jobs = fetch_job_openings()

    if not jobs:
        print("No job openings found.")
        return 0

    print(f"Found {len(jobs)} job opening(s)")

    if args.list:
        # List mode - just show what's available
        table = []
        for job in jobs:
            table.append([
                job.get('job_title', 'Untitled'),
                job.get('name', ''),
                job.get('status', '-'),
                'Yes' if job.get('publish') else 'No',
                job.get('department', '-'),
                job.get('location', '-'),
            ])
        headers = ['Title', 'ID', 'Status', 'Published', 'Department', 'Location']
        print()
        print(tabulate(table, headers=headers, tablefmt='simple'))
        return 0

    # Sync mode - fetch full details and sync each job
    if args.dry_run:
        print("DRY RUN - no files will be written")
    print()

    results = []
    for job in jobs:
        # Fetch full details for each job
        detail = fetch_job_detail(job['name'])
        if not detail:
            results.append({
                'status': 'error',
                'fidelity': '-',
                'file': '-',
                'title': job.get('job_title', 'Unknown'),
            })
            continue

        result = sync_job(
            detail, CONTENT_DIR,
            dry_run=args.dry_run,
            force=args.force,
            verbose=args.verbose,
        )
        results.append(result)

    # Unpublish closed jobs
    unpublished = unpublish_closed_jobs(jobs, CONTENT_DIR, dry_run=args.dry_run,
                                        verbose=args.verbose)
    results.extend(unpublished)

    # Print results table
    table = []
    for r in results:
        status = r.get('status', '-')
        fidelity = r.get('fidelity', '-')

        if fidelity == 'auto-reviewed':
            fidelity_str = '\u2713 auto-reviewed'
        elif fidelity == 'passed':
            fidelity_str = '\u2713 passed'
        elif fidelity == 'failed':
            fidelity_str = '\u2717 failed'
        else:
            fidelity_str = fidelity

        table.append([
            r.get('title', '-'),
            status,
            fidelity_str,
            r.get('file', '-'),
        ])

    headers = ['Title', 'Status', 'Fidelity', 'File']
    print()
    print(tabulate(table, headers=headers, tablefmt='simple'))

    # Summary
    new_count = sum(1 for r in results if r['status'] == 'new')
    updated_count = sum(1 for r in results if r['status'] == 'updated')
    unchanged_count = sum(1 for r in results if r['status'] == 'unchanged')
    unpub_count = sum(1 for r in results if r['status'] == 'unpublished')
    error_count = sum(1 for r in results if r['status'] == 'error')

    print()
    print(f"New: {new_count}, Updated: {updated_count}, Unchanged: {unchanged_count}, "
          f"Unpublished: {unpub_count}, Errors: {error_count}")

    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
