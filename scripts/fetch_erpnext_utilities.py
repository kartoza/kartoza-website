#!/usr/bin/env python3
"""Shared Hugo content-sync helpers for the ERPNext sync scripts in this
directory.

Covers slugifying titles, fidelity-checking local content against ERPNext,
reading/matching local Hugo files, stamping review fields, and converting
ERPNext HTML to Hugo markdown.
"""

import html2text
import re
import warnings
import yaml
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from datetime import datetime
from pathlib import Path

# Suppress XML parsing warning when using html.parser on content that looks
# like XML
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def normalize_for_comparison(content: str) -> str:
    """Normalize content for fidelity comparison, focusing on text only."""
    if not content:
        return ''

    # Remove Hugo shortcodes like {{< block >}} or {{< /block >}}
    content = re.sub(r'\{\{[<>%].*?[>%]\}\}', '', content)

    # Strip HTML tags but keep text content
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text(separator=' ')

    # Collapse whitespace (multiple spaces/newlines -> single space)
    text = re.sub(r'\s+', ' ', text)

    return text.strip().lower()


def check_fidelity(local_content: str, erpnext_content: str) -> bool:
    """Check if local and ERPNext content match, ignoring formatting."""
    return (
            normalize_for_comparison(local_content) ==
            normalize_for_comparison(erpnext_content)
    )


def read_local_file(filepath: Path) -> tuple[dict, str] | None:
    """Read a local Hugo file and extract front matter and content.

    Returns a tuple of (front_matter_dict, content_str), or None if the
    file doesn't exist.
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
    """Find a local Hugo file matching an ERPNext document.

    Matches by:
    1. erpnext_id in front matter (primary)
    2. Slugified title matching filename (fallback)
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


def update_review_fields(
        filepath: Path, front_matter: dict, content: str
) -> None:
    """Stamp reviewedBy/reviewedDate and rewrite an existing Hugo file."""
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
