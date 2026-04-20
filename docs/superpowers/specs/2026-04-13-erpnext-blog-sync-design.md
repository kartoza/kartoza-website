# ERPNext Blog Sync with Fidelity Checking

**Date:** 2026-04-13
**Status:** Approved
**Author:** Claude Code (with Tim Sutton)

## Overview

Enhance `fetch-erpnext-blogs.py` to sync blog articles from erp.kartoza.com to this Hugo site with automated fidelity checking and review marking. Articles that pass fidelity checks are automatically marked as reviewed and become visible on the blog listing page.

## Requirements

| Requirement | Decision |
|-------------|----------|
| Fidelity check | Automated text comparison (ignore formatting) |
| Source of truth | ERPNext (always overwrites Hugo on mismatch) |
| Review workflow | Auto-mark `reviewedBy: "Automated Check"` + `reviewedDate: <today>` when fidelity passes |
| Output | Status table (new, unchanged, updated, error) |
| Architecture | Enhance `fetch-erpnext-blogs.py`, call from `sync-content-from-erpnext.py` |

## Design

### Workflow & Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     fetch-erpnext-blogs.py                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Fetch blog list from ERPNext API                            │
│                    ↓                                            │
│  2. For each blog:                                              │
│     ├─ Fetch full content from ERPNext                          │
│     ├─ Check if local Hugo file exists                          │
│     │   ├─ NO  → Create new file, mark as "newly harvested"     │
│     │   └─ YES → Compare text content (fidelity check)          │
│     │            ├─ MATCH    → Mark as "fidelity passed"        │
│     │            └─ MISMATCH → Overwrite with ERPNext content   │
│     ├─ Auto-set reviewedBy + reviewedDate if fidelity passes    │
│     └─ Download images (existing behavior)                      │
│                    ↓                                            │
│  3. Output status table                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Key changes from current behavior:**

- Current: Skips existing files entirely
- New: Compares content and overwrites if ERPNext differs

**Statuses tracked:**

| Status | Meaning |
|--------|---------|
| `new` | Article didn't exist locally, created from ERPNext |
| `unchanged` | Local content matches ERPNext (fidelity passed) |
| `updated` | Local content differed, overwritten with ERPNext |
| `error` | Failed to fetch or process |

### Fidelity Checking

**Text normalization before comparison:**

```python
def normalize_for_comparison(content: str) -> str:
    """
    Normalize content for fidelity comparison.
    Focuses on TEXT content, ignores formatting/layout.
    """
    # 1. Strip HTML tags (keep text content)
    # 2. Remove Hugo shortcodes like {{< block >}}
    # 3. Collapse whitespace (multiple spaces/newlines → single space)
    # 4. Strip leading/trailing whitespace
    # 5. Lowercase for comparison

    return normalized_text
```

**Comparison method:**

```python
def check_fidelity(local_content: str, erpnext_content: str) -> bool:
    """
    Returns True if text content matches (fidelity passes).
    """
    local_norm = normalize_for_comparison(local_content)
    erpnext_norm = normalize_for_comparison(erpnext_content)

    return local_norm == erpnext_norm
```

**What's compared:**

- ✅ Body text content
- ✅ Headings text
- ❌ HTML formatting/tags
- ❌ Hugo shortcodes
- ❌ Whitespace/line breaks
- ❌ Front matter (compared separately for `erpnext_id` matching)

**Matching local files to ERPNext articles:**

- Primary: Match by `erpnext_id` field in front matter
- Fallback: Match by slugified title

### Front Matter Schema

**Required fields for a blog article to appear on the site:**

```yaml
---
title: "Article Title"
description: "Brief description"
date: 2024-06-17
author: "Author Name"
thumbnail: "/img/blog/article-image.png"
tags:
  - QGIS
  - Python
# ERPNext tracking
erpnext_id: "blog-post-name-from-erpnext"
erpnext_modified: "2024-06-17 14:30:00"
# Review fields (required for visibility on blog list)
reviewedBy: "Automated Check"
reviewedDate: 2026-04-13
---
```

**Field behaviors:**

| Field | Source | Behavior |
|-------|--------|----------|
| `title` | ERPNext | Overwritten on sync |
| `description` | ERPNext `blog_intro` | Overwritten on sync |
| `date` | ERPNext `published_on` | Overwritten on sync |
| `author` | ERPNext `blogger` | Overwritten on sync |
| `thumbnail` | ERPNext `featured_image` or default | Overwritten on sync |
| `tags` | ERPNext `blog_category` | Overwritten on sync |
| `erpnext_id` | ERPNext `name` | Set once, used for matching |
| `erpnext_modified` | ERPNext `modified` | Updated on each sync |
| `reviewedBy` | Script | Set to `"Automated Check"` when fidelity passes |
| `reviewedDate` | Script | Set to current date when fidelity passes |

### CLI Interface & Output

**Command line interface:**

```bash
# Full sync with fidelity checking (new default behavior)
./scripts/fetch-erpnext-blogs.py

# Dry run - show what would happen without writing files
./scripts/fetch-erpnext-blogs.py --dry-run

# List available blogs on ERPNext without syncing
./scripts/fetch-erpnext-blogs.py --list

# Skip image downloading (faster for testing)
./scripts/fetch-erpnext-blogs.py --skip-images

# Verbose output with fidelity details
./scripts/fetch-erpnext-blogs.py --verbose
```

**Status table output (using `tabulate`):**

```
════════════════════════════════════════════════════════════════════════════════
  ERPNEXT BLOG SYNC REPORT
  Source: https://erp.kartoza.com | Date: 2026-04-13
════════════════════════════════════════════════════════════════════════════════

  Title                                    Date        Author          Status      Fidelity
  ─────────────────────────────────────────────────────────────────────────────────────────
  Reflections on FOSDEM 2026               2026-02-15  Tim Sutton      new         ✓ auto-reviewed
  Building Energy Planning Capacity...     2026-01-20  Jane Doe        unchanged   ✓ passed
  How AI Tools Are Transforming...         2025-12-10  John Smith      updated     ✓ auto-reviewed
  Get Ready: Geospatial Hosting Is...      2025-11-05  Amy Wilson      unchanged   ✓ passed
  Agile Project Management for...          2025-10-22  Bob Jones       error       ✗ fetch failed

────────────────────────────────────────────────────────────────────────────────
  Summary: 127 total | 3 new | 120 unchanged | 3 updated | 1 error
════════════════════════════════════════════════════════════════════════════════
```

**Exit codes:**

- `0` - Success (all articles processed)
- `1` - Partial failure (some articles had errors)
- `2` - Complete failure (couldn't connect to ERPNext)

### Integration with sync-content-from-erpnext.py

**How the main sync script will call fetch-erpnext-blogs.py:**

```python
# In sync-content-from-erpnext.py

def sync_blog_content(self, download_images: bool = True) -> dict:
    """Sync blog articles by calling fetch-erpnext-blogs.py"""
    print("→ Syncing blog articles...")

    # Build command
    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "fetch-erpnext-blogs.py")]
    if not download_images:
        cmd.append("--skip-images")

    # Run and capture output
    result = subprocess.run(cmd, capture_output=True, text=True, env=os.environ)

    # Parse JSON summary from stdout (fetch script outputs JSON on last line)
    summary = json.loads(result.stdout.strip().split('\n')[-1])

    return summary
```

**fetch-erpnext-blogs.py will output:**

1. Human-readable table to stderr (always visible)
2. JSON summary to stdout (for programmatic consumption)

```python
# At end of fetch-erpnext-blogs.py
summary = {
    "total": 127,
    "new": 3,
    "unchanged": 120,
    "updated": 3,
    "errors": 1,
    "articles": [...]  # Full list with statuses
}
print(json.dumps(summary))  # To stdout for sync script
```

**Environment variables:**

- `ERPNEXT_URL` - ERPNext instance URL (default: `https://erp.kartoza.com`)

**Note:** No API keys required - all blog articles are public. Authentication is only needed for private content (not applicable to blogs).

## Future Work (Out of Scope)

- Blog card CSS layout changes (3 columns consistently) - to be addressed separately
- Image fidelity checking (comparing downloaded images)
- Manual review workflow override

## Dependencies

All dependencies are already available in `nix develop`:

- `requests` - HTTP requests to ERPNext API
- `pyyaml` - YAML front matter parsing/writing
- `beautifulsoup4` - HTML tag stripping for fidelity check
- `tabulate` - Status table output
- `python-dateutil` - Date parsing
