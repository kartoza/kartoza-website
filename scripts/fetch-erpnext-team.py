#!/usr/bin/env python3
"""
Fetch team member information from ERPNext.
Adds new team members and marks departed ones as inactive.

Pulls from the Employee doctype (status=Active), matching the fields used
by Kartoza's ERPNext employee profile web page: employee_name, last_name,
designation, bio, image/avatar, github_user_name, linked_in_user_name,
custom_nickname, custom_show_nickname_on_website.

Environment variables:
    ERPNEXT_URL: ERPNext instance URL (default: https://erp.kartoza.com)
    ERPNEXT_API_KEY, ERPNEXT_API_SECRET: API credentials (required)
    ERPNEXT_TEAM_DOCTYPE: ERPNext doctype to query (default: Employee)

Usage:
    python3 fetch-erpnext-team.py [--list] [--dry-run]

Options:
    --list      List team members from ERPNext without downloading
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

from fetch_erpnext_client import ERPNextClient

# ERPNext configuration
ERPNEXT = ERPNextClient()
TEAM_DOCTYPE = os.environ.get("ERPNEXT_TEAM_DOCTYPE", "Employee")
TEAM_FIELDS = [
    "name", "employee_name", "last_name", "designation", "bio", "image",
    "avatar", "github_user_name", "linked_in_user_name",
    "custom_nickname", "custom_show_nickname_on_website",
]
PROJECT_ROOT = Path(__file__).parent.parent
TEAM_CONTENT_DIR = PROJECT_ROOT / "content" / "the_team"
TEAM_IMAGE_DIR = PROJECT_ROOT / "static" / "img" / "team"
PLACEHOLDER_IMAGE = "/img/team/placeholder.jpg"


def download_team_photo(url: str | None, slug: str) -> str | None:
    """Download an employee's ERPNext photo into static/img/team/.

    :param url: The image/avatar path from ERPNext (e.g. /private/files/x.png).
    :param slug: The team member's slug, used as the local filename.

    :returns: Local Hugo path (e.g. /img/team/ariel.png), or None on failure.
    """
    if not url:
        return None

    ext = Path(url).suffix or ".jpg"
    filename = f"{slug}{ext}"
    target_path = TEAM_IMAGE_DIR / filename
    local_url = f"/img/team/{filename}"

    if target_path.exists():
        return local_url

    full_url = f"{ERPNEXT.base_url}{url}" if url.startswith("/") else url

    try:
        response = ERPNEXT.get(full_url)
        response.raise_for_status()
        TEAM_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(response.content)
        return local_url
    except requests.RequestException as exc:
        print(f"Warning: Failed to download photo for '{slug}': {exc}", file=sys.stderr)
        return None


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text


def first_sentence(text: str) -> str:
    """Return the first sentence of a block of text, for use as a short teaser."""
    text = (text or '').strip()
    if not text:
        return ''
    match = re.search(r'^.*?[.!?](?=\s|$)', text, re.DOTALL)
    sentence = match.group(0) if match else text
    return re.sub(r'\s+', ' ', sentence).strip()


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


EXCLUDED_DESIGNATIONS = {"sub-contractor"}
EXCLUDED_NAME_PATTERN = re.compile(r'\btest\b', re.IGNORECASE)


def is_publishable(member: dict) -> bool:
    """Return False for records that should never appear on the website.

    Excludes sub-contractors and employees whose name contains the
    standalone word "test" (dummy/test records, e.g. "Juanique Test").
    """
    designation = (member.get("designation") or "").strip().lower()
    if designation in EXCLUDED_DESIGNATIONS:
        return False
    if EXCLUDED_NAME_PATTERN.search(member.get("employee_name") or ""):
        return False
    return True


def fetch_team_from_erpnext() -> list:
    """Fetch active employees from ERPNext to publish as website team members.

    Excludes sub-contractors and dummy/test records - see is_publishable().
    """
    url = f"/api/resource/{TEAM_DOCTYPE}"
    params = {
        "fields": json.dumps(TEAM_FIELDS),
        "filters": json.dumps([["status", "=", "Active"]]),
        "limit_page_length": 0,
    }

    try:
        response = ERPNEXT.get(url, params=params)
        response.raise_for_status()
        members = response.json().get("data", [])
        return [m for m in members if is_publishable(m)]
    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else None
        if status_code in (401, 403):
            print(
                f"Warning: Authentication/permission error fetching "
                f"'{TEAM_DOCTYPE}' (HTTP {status_code}). "
                "Check ERPNEXT_API_KEY/ERPNEXT_API_SECRET and that the "
                "doctype name in ERPNEXT_TEAM_DOCTYPE is correct.",
                file=sys.stderr,
            )
        else:
            print(f"Warning: Could not fetch from ERPNext API (HTTP {status_code}): {exc}", file=sys.stderr)
        return []
    except requests.RequestException as exc:
        print(f"Warning: Could not fetch from ERPNext API: {exc}", file=sys.stderr)
        return []


def display_name(member: dict) -> str:
    """Return the public display name, honouring the nickname-on-website flag.

    Mirrors the name logic in Kartoza's ERPNext employee profile web page.
    """
    if member.get("custom_show_nickname_on_website") and member.get("custom_nickname"):
        return f"{member['custom_nickname']} {member.get('last_name', '')}".strip()
    return member.get("employee_name", "Team Member")


def get_existing_team_members() -> dict:
    """Get existing team member files and their status, keyed by erpnext_id.

    Files without an erpnext_id (not yet linked to an ERPNext record) are
    keyed by their file stem instead, and left alone by the departure
    check, since there's nothing reliable to match them against.
    """
    team_members = {}

    if not TEAM_CONTENT_DIR.exists():
        return team_members

    for md_file in TEAM_CONTENT_DIR.glob("*.md"):
        if md_file.name == "_index.md":
            continue

        result = read_local_file(md_file)
        if not result:
            continue
        front_matter, _ = result

        name = front_matter.get("title")
        if not name:
            continue

        erpnext_id = front_matter.get("erpnext_id")
        is_hidden = bool(front_matter.get("hidden"))

        team_members[erpnext_id or md_file.stem] = {
            "name": name,
            "file": md_file,
            "erpnext_id": erpnext_id,
            "is_active": not is_hidden,
            "slug": md_file.stem,
        }

    return team_members


def generate_team_content(member: dict) -> str:
    """Generate the content section for a team member page.

    Plain bio prose only - matching how hand-written team pages are
    written. layouts/the_team/single.html already renders its own "About"
    heading and hero title/role/bio, so no shortcode or heading belongs
    in the body content itself.
    """
    bio = member.get('bio') or 'Bio coming soon.'
    return f"{bio}\n"


def create_team_member_page(member: dict, dry_run: bool = False) -> Path | None:
    """Create a new team member page, or update one awaiting first review.

    Returns None (and does nothing) if the target slug is already taken by
    a page linked to a *different* ERPNext record - that's a same-name
    collision (e.g. two Employee records for one person, or an unrelated
    person with the same name), not this member, and must never be
    overwritten.
    """
    name = display_name(member)
    slug = slugify(name)
    filepath = TEAM_CONTENT_DIR / f"{slug}.md"

    erpnext_content = generate_team_content(member)

    if filepath.exists():
        result = read_local_file(filepath)
        if result:
            local_frontmatter, local_content = result
            existing_id = local_frontmatter.get('erpnext_id')
            if existing_id and existing_id != member.get('name'):
                print(
                    f"Skipped (slug '{slug}' already belongs to ERPNext "
                    f"record {existing_id}): {filepath.name}"
                )
                return None

            if check_fidelity(local_content, erpnext_content):
                # Content matches - fidelity passed
                if not local_frontmatter.get('reviewedBy'):
                    if not dry_run:
                        local_frontmatter['reviewedBy'] = 'Automated Check'
                        local_frontmatter['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')
                        local_frontmatter['erpnext_id'] = member.get('name')
                        file_content = "---\n"
                        file_content += yaml.dump(local_frontmatter, default_flow_style=False, allow_unicode=True)
                        file_content += "---\n\n"
                        file_content += local_content.strip()
                        file_content += "\n"
                        filepath.write_text(file_content)
                print(f"Unchanged (fidelity passed): {filepath.name}")
                return filepath

    # Default template, matching the frontmatter layouts/the_team/single.html renders.
    github = member.get('github_user_name') or ''
    linkedin_user = member.get('linked_in_user_name') or ''
    linkedin = f'https://www.linkedin.com/in/{linkedin_user}' if linkedin_user else ''
    photo_url = member.get('image') or member.get('avatar')
    image = (photo_url and download_team_photo(photo_url, slug)) or PLACEHOLDER_IMAGE

    bio_teaser = first_sentence(member.get('bio')) or 'Bio coming soon.'

    content = f'''---
title: "{name}"
erpnext_id: "{member.get('name', '')}"
role: "{member.get('designation') or 'Team Member'}"
image: "{image}"
bio: "{bio_teaser}"
github: "{github}"
linkedin: "{linkedin}"
weight: 100
draft: false
reviewedBy: "Automated Check"
reviewedDate: {datetime.now().strftime('%Y-%m-%d')}
---

{erpnext_content}'''

    if dry_run:
        print(f"Would create: {filepath}")
    else:
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(content)
        print(f"Created: {filepath}")

    return filepath


def mark_member_departed(member_info: dict, dry_run: bool = False):
    """Hide a departed team member from the website's team listing."""
    filepath = member_info["file"]
    content = filepath.read_text()

    if "hidden:" not in content:
        content = content.replace("---\n", "---\nhidden: true\n", 1)

        if dry_run:
            print(f"Would mark as hidden (departed): {filepath}")
        else:
            filepath.write_text(content)
            print(f"Marked as hidden (departed): {filepath}")


def list_team_members():
    """List all team members from ERPNext and local."""
    print("=" * 60)
    print("Team Members")
    print("=" * 60)

    print("\nERPNext Team Members:")
    print("-" * 40)
    erpnext_team = fetch_team_from_erpnext()
    if erpnext_team:
        for member in erpnext_team:
            name = display_name(member)
            role = member.get("designation", "")
            print(f"  - {name} ({role})")
    else:
        print("  No team members fetched from ERPNext")
        print("  (API may require authentication)")

    print("\nLocal Team Members:")
    print("-" * 40)
    local_team = get_existing_team_members()
    active = [m for m in local_team.values() if m["is_active"]]
    departed = [m for m in local_team.values() if not m["is_active"]]

    print(f"\n  Active ({len(active)}):")
    for member in sorted(active, key=lambda x: x["name"]):
        print(f"    - {member['name']}")

    if departed:
        print(f"\n  Departed ({len(departed)}):")
        for member in sorted(departed, key=lambda x: x["name"]):
            print(f"    - {member['name']}")


def sync_team_members(dry_run: bool = False):
    """Sync team members between ERPNext and local content."""
    print("=" * 60)
    print("Syncing Team Members")
    print("=" * 60)

    erpnext_team = fetch_team_from_erpnext()
    local_team = get_existing_team_members()

    if not erpnext_team:
        print("\nWarning: No team members fetched from ERPNext")
        print("This may be because:")
        print("  - ERPNext API requires authentication")
        print("  - The endpoint structure is different")
        print("\nNo changes will be made.")
        return

    # Convert ERPNext team to a lookup by ERPNext record id (stable, unlike names)
    erpnext_by_id = {member["name"]: member for member in erpnext_team if member.get("name")}

    # Find new team members (in ERPNext but not already linked to a local file)
    new_members = [
        member for erpnext_id, member in erpnext_by_id.items()
        if erpnext_id not in local_team
    ]

    # Find departed team members (linked locally, active, but no longer in
    # the active ERPNext list). Local files with no stored erpnext_id yet
    # are skipped - there's nothing reliable to match them against.
    departed = [
        info for info in local_team.values()
        if info["erpnext_id"] and info["is_active"] and info["erpnext_id"] not in erpnext_by_id
    ]

    print(f"\nNew team members to add: {len(new_members)}")
    for member in new_members:
        name = display_name(member)
        print(f"  + {name}")
        create_team_member_page(member, dry_run)

    print(f"\nDeparted team members to mark: {len(departed)}")
    for info in departed:
        print(f"  - {info['name']}")
        mark_member_departed(info, dry_run)

    if not new_members and not departed:
        print("\nNo changes needed - team is in sync")


def main():
    parser = argparse.ArgumentParser(description="Fetch team members from ERPNext")
    parser.add_argument("--list", action="store_true", help="List team members without syncing")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without making them")
    args = parser.parse_args()

    if args.list:
        list_team_members()
    else:
        sync_team_members(args.dry_run)


if __name__ == "__main__":
    main()
