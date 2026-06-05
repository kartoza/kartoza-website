#!/usr/bin/env python3
"""
Wrapper script to sync all content from ERPNext.
This allows adding new content type fetchers without changing GitHub Actions.

Usage:
    python3 sync-erpnext-content.py [--dry-run] [--list]

Options:
    --dry-run   Preview what would be synced without making changes
    --list      List available content on ERPNext without downloading
"""

import subprocess
import sys
from pathlib import Path


# Define all ERPNext content fetchers to run
# Add new fetcher scripts here as they are created
FETCHERS = [
    {
        "name": "Blog Posts",
        "script": "fetch-erpnext-blogs.py",
        "description": "Fetches blog posts from ERPNext"
    },
    {
        "name": "Portfolio Items",
        "script": "fetch-erpnext-portfolio.py",
        "description": "Fetches portfolio/project items from ERPNext"
    },
    {
        "name": "Team Members",
        "script": "fetch-erpnext-team.py",
        "description": "Syncs team members - adds new, marks departed"
    },
    {
        "name": "Training Courses",
        "script": "fetch-erpnext-training.py",
        "description": "Fetches training courses and scheduled events"
    },
    {
        "name": "Standalone Pages",
        "script": "fetch-erpnext-pages.py",
        "description": "Fetches standalone pages (policies, resources, etc.)"
    },
    {
        "name": "Job Opportunities",
        "script": "fetch-erpnext-jobs.py",
        "description": "Fetches job openings with publish/unpublish support"
    },
]


def run_fetcher(script_path: Path, args: list) -> bool:
    """Run a fetcher script and return True if successful."""
    try:
        cmd = [sys.executable, str(script_path)] + args
        result = subprocess.run(cmd, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {script_path.name}: {e}")
        return False


def main():
    scripts_dir = Path(__file__).parent
    args = sys.argv[1:]

    print("=" * 60)
    print("ERPNext Content Sync")
    print("=" * 60)
    print()

    if "--list" in args:
        print("Listing available content from ERPNext...")
        print()
    elif "--dry-run" in args:
        print("Running in dry-run mode (no changes will be made)")
        print()
    else:
        print("Syncing new content from ERPNext...")
        print()

    success_count = 0
    failure_count = 0

    for fetcher in FETCHERS:
        script_path = scripts_dir / fetcher["script"]

        if not script_path.exists():
            print(f"Warning: {fetcher['script']} not found, skipping {fetcher['name']}")
            failure_count += 1
            continue

        print("-" * 60)
        print(f"Fetching: {fetcher['name']}")
        print(f"Script: {fetcher['script']}")
        print(f"Description: {fetcher['description']}")
        print("-" * 60)

        if run_fetcher(script_path, args):
            success_count += 1
            print(f"✓ {fetcher['name']} completed successfully")
        else:
            failure_count += 1
            print(f"✗ {fetcher['name']} failed")

        print()

    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Total: {len(FETCHERS)}")

    return 0 if failure_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
