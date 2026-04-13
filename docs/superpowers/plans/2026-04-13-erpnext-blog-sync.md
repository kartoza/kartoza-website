# ERPNext Blog Sync with Fidelity Checking - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enhance `fetch-erpnext-blogs.py` to sync blog articles from ERPNext with automated fidelity checking and review marking.

**Architecture:** Modify the existing script to compare local Hugo content with ERPNext source (text-only, ignoring formatting), auto-overwrite when content differs (ERPNext is authoritative), and auto-mark articles as reviewed when fidelity passes. Output includes a rich status table and JSON summary for programmatic use.

**Tech Stack:** Python 3, requests, pyyaml, beautifulsoup4, tabulate (all available in nix develop)

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `scripts/fetch-erpnext-blogs.py` | Modify | Add fidelity checking, review marking, enhanced output |
| `scripts/sync-content-from-erpnext.py` | Modify | Call fetch-erpnext-blogs.py via subprocess |
| `scripts/tests/test_fetch_erpnext_blogs.py` | Create | Unit tests for fidelity checking functions |

---

## Task 1: Add Text Normalization Function

**Files:**

- Modify: `scripts/fetch-erpnext-blogs.py:1-30` (add imports and new function)
- Create: `scripts/tests/test_fetch_erpnext_blogs.py`

- [ ] **Step 1: Create test directory and initial test file**

```bash
mkdir -p scripts/tests
touch scripts/tests/__init__.py
```

- [ ] **Step 2: Write failing tests for normalize_for_comparison**

Create `scripts/tests/test_fetch_erpnext_blogs.py`:

```python
#!/usr/bin/env python3
"""Tests for fetch-erpnext-blogs.py fidelity checking functions."""

import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import will fail until we implement
from importlib import import_module


def get_module():
    """Import the fetch script as a module."""
    spec = import_module('fetch-erpnext-blogs')
    return spec


class TestNormalizeForComparison:
    """Tests for normalize_for_comparison function."""

    def test_strips_html_tags(self):
        module = get_module()
        html = "<p>Hello <strong>world</strong></p>"
        result = module.normalize_for_comparison(html)
        assert "hello world" == result

    def test_removes_hugo_shortcodes(self):
        module = get_module()
        content = '{{< block title="Test" >}}Hello{{< /block >}}'
        result = module.normalize_for_comparison(content)
        assert "hello" == result

    def test_collapses_whitespace(self):
        module = get_module()
        content = "Hello    \n\n   world"
        result = module.normalize_for_comparison(content)
        assert "hello world" == result

    def test_lowercases_text(self):
        module = get_module()
        content = "Hello WORLD"
        result = module.normalize_for_comparison(content)
        assert "hello world" == result

    def test_empty_string(self):
        module = get_module()
        result = module.normalize_for_comparison("")
        assert "" == result

    def test_complex_html(self):
        module = get_module()
        html = """
        <div class="content">
            <h2>Title</h2>
            <p>First paragraph with <a href="#">link</a>.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
            </ul>
        </div>
        """
        result = module.normalize_for_comparison(html)
        assert "title first paragraph with link. item 1 item 2" == result
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py -v
```

Expected: FAIL with import error or AttributeError (function doesn't exist)

- [ ] **Step 4: Add imports and implement normalize_for_comparison**

Edit `scripts/fetch-erpnext-blogs.py`, add after line 24 (after `from dateutil import parser as date_parser`):

```python
from bs4 import BeautifulSoup
from tabulate import tabulate
import json
```

Add after the `slugify` function (after line 47):

```python
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

    # Collapse whitespace (multiple spaces/newlines → single space)
    text = re.sub(r'\s+', ' ', text)

    # Strip leading/trailing whitespace and lowercase
    return text.strip().lower()
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestNormalizeForComparison -v
```

Expected: All 6 tests PASS

- [ ] **Step 6: Commit**

```bash
git add scripts/fetch-erpnext-blogs.py scripts/tests/
git commit -m "feat: add normalize_for_comparison for fidelity checking"
```

---

## Task 2: Add Fidelity Check Function

**Files:**

- Modify: `scripts/fetch-erpnext-blogs.py` (add check_fidelity function)
- Modify: `scripts/tests/test_fetch_erpnext_blogs.py` (add tests)

- [ ] **Step 1: Write failing tests for check_fidelity**

Add to `scripts/tests/test_fetch_erpnext_blogs.py`:

```python
class TestCheckFidelity:
    """Tests for check_fidelity function."""

    def test_identical_content_returns_true(self):
        module = get_module()
        local = "Hello world"
        remote = "Hello world"
        assert module.check_fidelity(local, remote) is True

    def test_different_content_returns_false(self):
        module = get_module()
        local = "Hello world"
        remote = "Goodbye world"
        assert module.check_fidelity(local, remote) is False

    def test_ignores_html_formatting(self):
        module = get_module()
        local = "Hello world"
        remote = "<p>Hello <strong>world</strong></p>"
        assert module.check_fidelity(local, remote) is True

    def test_ignores_whitespace_differences(self):
        module = get_module()
        local = "Hello world"
        remote = "Hello    \n\n   world"
        assert module.check_fidelity(local, remote) is True

    def test_ignores_case_differences(self):
        module = get_module()
        local = "hello world"
        remote = "HELLO WORLD"
        assert module.check_fidelity(local, remote) is True

    def test_ignores_hugo_shortcodes(self):
        module = get_module()
        local = "Hello world"
        remote = '{{< block >}}Hello world{{< /block >}}'
        assert module.check_fidelity(local, remote) is True
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestCheckFidelity -v
```

Expected: FAIL with AttributeError (function doesn't exist)

- [ ] **Step 3: Implement check_fidelity**

Add after `normalize_for_comparison` function in `scripts/fetch-erpnext-blogs.py`:

```python
def check_fidelity(local_content: str, erpnext_content: str) -> bool:
    """
    Check if local and ERPNext content match (fidelity check).

    Returns True if text content matches (ignoring formatting).
    """
    local_norm = normalize_for_comparison(local_content)
    erpnext_norm = normalize_for_comparison(erpnext_content)
    return local_norm == erpnext_norm
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestCheckFidelity -v
```

Expected: All 6 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch-erpnext-blogs.py scripts/tests/test_fetch_erpnext_blogs.py
git commit -m "feat: add check_fidelity function for content comparison"
```

---

## Task 3: Add Local File Reading and Matching

**Files:**

- Modify: `scripts/fetch-erpnext-blogs.py` (add functions to read local files)
- Modify: `scripts/tests/test_fetch_erpnext_blogs.py` (add tests)

- [ ] **Step 1: Write failing tests for read_local_blog**

Add to `scripts/tests/test_fetch_erpnext_blogs.py`:

```python
import tempfile
import os


class TestReadLocalBlog:
    """Tests for read_local_blog function."""

    def test_reads_frontmatter_and_content(self):
        module = get_module()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("""---
title: "Test Article"
erpnext_id: "test-123"
---

This is the content.
""")
            f.flush()
            try:
                front_matter, content = module.read_local_blog(Path(f.name))
                assert front_matter['title'] == "Test Article"
                assert front_matter['erpnext_id'] == "test-123"
                assert "This is the content." in content
            finally:
                os.unlink(f.name)

    def test_returns_none_for_missing_file(self):
        module = get_module()
        result = module.read_local_blog(Path("/nonexistent/file.md"))
        assert result is None

    def test_handles_file_without_frontmatter(self):
        module = get_module()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("Just plain content without frontmatter.")
            f.flush()
            try:
                result = module.read_local_blog(Path(f.name))
                assert result is not None
                front_matter, content = result
                assert front_matter == {}
                assert "Just plain content" in content
            finally:
                os.unlink(f.name)
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestReadLocalBlog -v
```

Expected: FAIL with AttributeError

- [ ] **Step 3: Implement read_local_blog**

Add after `check_fidelity` function in `scripts/fetch-erpnext-blogs.py`:

```python
def read_local_blog(filepath: Path) -> tuple[dict, str] | None:
    """
    Read a local Hugo blog file and extract front matter and content.

    Returns:
        Tuple of (front_matter_dict, content_str) or None if file doesn't exist
    """
    if not filepath.exists():
        return None

    try:
        text = filepath.read_text()
    except (IOError, OSError):
        return None

    # Check for front matter delimiter
    if not text.startswith('---'):
        return {}, text

    # Find end of front matter
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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestReadLocalBlog -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch-erpnext-blogs.py scripts/tests/test_fetch_erpnext_blogs.py
git commit -m "feat: add read_local_blog to parse Hugo markdown files"
```

---

## Task 4: Add Find Local File Function

**Files:**

- Modify: `scripts/fetch-erpnext-blogs.py` (add find_local_file function)
- Modify: `scripts/tests/test_fetch_erpnext_blogs.py` (add tests)

- [ ] **Step 1: Write failing tests for find_local_file**

Add to `scripts/tests/test_fetch_erpnext_blogs.py`:

```python
class TestFindLocalFile:
    """Tests for find_local_file function."""

    def test_finds_by_erpnext_id(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            # Create file with erpnext_id
            (content_dir / "my-article.md").write_text("""---
title: "My Article"
erpnext_id: "blog-post-123"
---
Content here.
""")
            result = module.find_local_file(content_dir, "blog-post-123", "Different Title")
            assert result is not None
            assert result.name == "my-article.md"

    def test_finds_by_slugified_title(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            # Create file matching slugified title (no erpnext_id)
            (content_dir / "my-test-article.md").write_text("""---
title: "My Test Article"
---
Content here.
""")
            result = module.find_local_file(content_dir, "unknown-id", "My Test Article")
            assert result is not None
            assert result.name == "my-test-article.md"

    def test_returns_none_when_not_found(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            result = module.find_local_file(content_dir, "unknown", "Unknown Title")
            assert result is None
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestFindLocalFile -v
```

Expected: FAIL with AttributeError

- [ ] **Step 3: Implement find_local_file**

Add after `read_local_blog` function in `scripts/fetch-erpnext-blogs.py`:

```python
def find_local_file(content_dir: Path, erpnext_id: str, title: str) -> Path | None:
    """
    Find a local Hugo file matching the ERPNext article.

    Matches by:
    1. erpnext_id in front matter (primary)
    2. Slugified title matching filename (fallback)

    Returns:
        Path to matching file or None
    """
    # First, try to find by erpnext_id in front matter
    for filepath in content_dir.glob('*.md'):
        if filepath.name == '_index.md':
            continue
        result = read_local_blog(filepath)
        if result:
            front_matter, _ = result
            if front_matter.get('erpnext_id') == erpnext_id:
                return filepath

    # Fallback: match by slugified title
    expected_filename = f"{slugify(title)}.md"
    expected_path = content_dir / expected_filename
    if expected_path.exists():
        return expected_path

    return None
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestFindLocalFile -v
```

Expected: All 3 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch-erpnext-blogs.py scripts/tests/test_fetch_erpnext_blogs.py
git commit -m "feat: add find_local_file to match ERPNext articles with local files"
```

---

## Task 5: Update Front Matter Generation with Review Fields

**Files:**

- Modify: `scripts/fetch-erpnext-blogs.py` (update blog_to_hugo_frontmatter)

- [ ] **Step 1: Write failing tests for review fields**

Add to `scripts/tests/test_fetch_erpnext_blogs.py`:

```python
from datetime import date


class TestBlogToHugoFrontmatter:
    """Tests for blog_to_hugo_frontmatter function."""

    def test_includes_review_fields_when_requested(self):
        module = get_module()
        blog = {
            'name': 'test-blog',
            'title': 'Test Blog',
            'published_on': '2024-01-15',
            'blogger': 'Test Author',
            'modified': '2024-01-15 10:00:00',
        }
        result = module.blog_to_hugo_frontmatter(blog, mark_reviewed=True)
        assert result['reviewedBy'] == 'Automated Check'
        assert result['reviewedDate'] == date.today().isoformat()

    def test_excludes_review_fields_when_not_requested(self):
        module = get_module()
        blog = {
            'name': 'test-blog',
            'title': 'Test Blog',
            'published_on': '2024-01-15',
            'blogger': 'Test Author',
            'modified': '2024-01-15 10:00:00',
        }
        result = module.blog_to_hugo_frontmatter(blog, mark_reviewed=False)
        assert 'reviewedBy' not in result
        assert 'reviewedDate' not in result
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestBlogToHugoFrontmatter -v
```

Expected: FAIL (TypeError - unexpected keyword argument)

- [ ] **Step 3: Update blog_to_hugo_frontmatter**

Replace the existing `blog_to_hugo_frontmatter` function in `scripts/fetch-erpnext-blogs.py`:

```python
def blog_to_hugo_frontmatter(blog: dict, mark_reviewed: bool = False) -> dict:
    """Convert ERPNext blog to Hugo front matter."""
    # Parse date
    pub_date = blog.get('published_on') or blog.get('creation')
    if pub_date:
        try:
            dt = date_parser.parse(pub_date)
            date_str = dt.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            date_str = datetime.now().strftime('%Y-%m-%d')
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')

    # Build front matter
    front_matter = {
        'title': blog.get('title', 'Untitled'),
        'description': blog.get('blog_intro', '')[:200] if blog.get('blog_intro') else '',
        'date': date_str,
        'author': blog.get('blogger', 'Kartoza'),
        'thumbnail': '/img/blog/placeholder.png',
        'tags': [],
        'erpnext_id': blog.get('name', ''),
        'erpnext_modified': blog.get('modified', ''),
    }

    # Add category as tag
    if blog.get('blog_category'):
        front_matter['tags'].append(blog['blog_category'])

    # Add review fields if requested
    if mark_reviewed:
        front_matter['reviewedBy'] = 'Automated Check'
        front_matter['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')

    return front_matter
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestBlogToHugoFrontmatter -v
```

Expected: All 2 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch-erpnext-blogs.py scripts/tests/test_fetch_erpnext_blogs.py
git commit -m "feat: add mark_reviewed parameter to blog_to_hugo_frontmatter"
```

---

## Task 6: Rewrite sync_blog Function with Fidelity Checking

**Files:**

- Modify: `scripts/fetch-erpnext-blogs.py` (replace create_hugo_file with sync_blog)

- [ ] **Step 1: Write failing tests for sync_blog**

Add to `scripts/tests/test_fetch_erpnext_blogs.py`:

```python
class TestSyncBlog:
    """Tests for sync_blog function."""

    def test_creates_new_file(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            blog = {
                'name': 'new-blog',
                'title': 'New Blog Article',
                'content': '<p>This is new content.</p>',
                'published_on': '2024-01-15',
                'blogger': 'Author',
                'modified': '2024-01-15 10:00:00',
            }
            result = module.sync_blog(blog, content_dir, dry_run=False)
            assert result['status'] == 'new'
            assert result['fidelity'] == 'auto-reviewed'
            # Check file was created
            assert (content_dir / 'new-blog-article.md').exists()

    def test_unchanged_when_fidelity_passes(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            # Create existing file with matching content
            (content_dir / 'existing-article.md').write_text("""---
title: "Existing Article"
erpnext_id: "existing-blog"
reviewedBy: "Previous Reviewer"
reviewedDate: "2024-01-01"
---

This is the content.
""")
            blog = {
                'name': 'existing-blog',
                'title': 'Existing Article',
                'content': 'This is the content.',
                'published_on': '2024-01-15',
                'blogger': 'Author',
                'modified': '2024-01-15 10:00:00',
            }
            result = module.sync_blog(blog, content_dir, dry_run=False)
            assert result['status'] == 'unchanged'
            assert result['fidelity'] == 'passed'

    def test_updates_when_fidelity_fails(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            # Create existing file with different content
            (content_dir / 'old-article.md').write_text("""---
title: "Old Article"
erpnext_id: "old-blog"
---

Old content that differs.
""")
            blog = {
                'name': 'old-blog',
                'title': 'Old Article',
                'content': '<p>New content from ERPNext.</p>',
                'published_on': '2024-01-15',
                'blogger': 'Author',
                'modified': '2024-01-15 10:00:00',
            }
            result = module.sync_blog(blog, content_dir, dry_run=False)
            assert result['status'] == 'updated'
            assert result['fidelity'] == 'auto-reviewed'
            # Check file was overwritten
            content = (content_dir / 'old-article.md').read_text()
            assert 'New content from ERPNext' in content

    def test_dry_run_does_not_write(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            blog = {
                'name': 'dry-run-blog',
                'title': 'Dry Run Article',
                'content': 'Content.',
                'published_on': '2024-01-15',
                'blogger': 'Author',
                'modified': '2024-01-15 10:00:00',
            }
            result = module.sync_blog(blog, content_dir, dry_run=True)
            assert result['status'] == 'new'
            # File should NOT exist
            assert not (content_dir / 'dry-run-article.md').exists()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestSyncBlog -v
```

Expected: FAIL with AttributeError

- [ ] **Step 3: Implement sync_blog function**

Add after `find_local_file` function in `scripts/fetch-erpnext-blogs.py`:

```python
def sync_blog(blog: dict, content_dir: Path, dry_run: bool = False) -> dict:
    """
    Sync a single blog article from ERPNext to Hugo.

    Performs fidelity checking and updates review fields.

    Returns:
        Dict with 'status' and 'fidelity' keys
    """
    erpnext_id = blog.get('name', '')
    title = blog.get('title', 'Untitled')
    erpnext_content = blog.get('content') or blog.get('content_html') or ''

    # Find existing local file
    local_file = find_local_file(content_dir, erpnext_id, title)

    if local_file:
        # File exists - check fidelity
        result = read_local_blog(local_file)
        if result:
            local_frontmatter, local_content = result
            if check_fidelity(local_content, erpnext_content):
                # Content matches - fidelity passed
                # Update review fields if not already set
                if not local_frontmatter.get('reviewedBy'):
                    if not dry_run:
                        _update_review_fields(local_file, local_frontmatter, local_content)
                return {'status': 'unchanged', 'fidelity': 'passed', 'file': local_file.name}

        # Content differs - overwrite with ERPNext
        status = 'updated'
        filepath = local_file
    else:
        # New file
        status = 'new'
        slug = slugify(title)
        filepath = content_dir / f"{slug}.md"

    # Generate content
    front_matter = blog_to_hugo_frontmatter(blog, mark_reviewed=True)
    content = blog_to_hugo_content(blog)

    # Build file content
    file_content = "---\n"
    file_content += yaml.dump(front_matter, default_flow_style=False, allow_unicode=True)
    file_content += "---\n\n"
    file_content += content
    file_content += "\n"

    if not dry_run:
        filepath.write_text(file_content)

    return {'status': status, 'fidelity': 'auto-reviewed', 'file': filepath.name}


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
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py::TestSyncBlog -v
```

Expected: All 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add scripts/fetch-erpnext-blogs.py scripts/tests/test_fetch_erpnext_blogs.py
git commit -m "feat: add sync_blog with fidelity checking and review marking"
```

---

## Task 7: Update Output with Rich Status Table

**Files:**

- Modify: `scripts/fetch-erpnext-blogs.py` (replace print_table with print_status_table)

- [ ] **Step 1: Replace print_table function**

Replace the `print_table` function in `scripts/fetch-erpnext-blogs.py`:

```python
def print_status_table(results: list[dict], dry_run: bool = False) -> None:
    """Print a rich status table of sync results to stderr."""
    if not results:
        print("\nNo blogs found.", file=sys.stderr)
        return

    # Prepare table data
    table_data = []
    for r in results:
        title = r['title'][:40] + ('...' if len(r['title']) > 40 else '')
        status = r['status']
        fidelity = r.get('fidelity', '-')

        # Format fidelity with symbols
        if fidelity == 'auto-reviewed':
            fidelity_str = '✓ auto-reviewed'
        elif fidelity == 'passed':
            fidelity_str = '✓ passed'
        elif fidelity == 'failed':
            fidelity_str = '✗ failed'
        else:
            fidelity_str = fidelity

        table_data.append([
            title,
            r.get('date', '-')[:10],
            r.get('author', '-')[:15],
            status,
            fidelity_str
        ])

    # Print header
    header = "ERPNEXT BLOG SYNC REPORT"
    if dry_run:
        header += " (DRY RUN)"

    print("\n" + "=" * 80, file=sys.stderr)
    print(f"  {header}", file=sys.stderr)
    print(f"  Source: {ERPNEXT_URL} | Date: {datetime.now().strftime('%Y-%m-%d')}", file=sys.stderr)
    print("=" * 80, file=sys.stderr)

    # Print table using tabulate
    headers = ['Title', 'Date', 'Author', 'Status', 'Fidelity']
    print(tabulate(table_data, headers=headers, tablefmt='simple'), file=sys.stderr)

    # Print summary
    print("-" * 80, file=sys.stderr)
    new_count = sum(1 for r in results if r['status'] == 'new')
    unchanged_count = sum(1 for r in results if r['status'] == 'unchanged')
    updated_count = sum(1 for r in results if r['status'] == 'updated')
    error_count = sum(1 for r in results if r['status'] == 'error')

    print(f"  Summary: {len(results)} total | {new_count} new | {unchanged_count} unchanged | {updated_count} updated | {error_count} errors", file=sys.stderr)
    print("=" * 80, file=sys.stderr)
```

- [ ] **Step 2: Verify table output manually**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command python3 -c "
from scripts import __init__
# Quick manual test of tabulate
from tabulate import tabulate
data = [['Test Article', '2024-01-15', 'Author', 'new', '✓ auto-reviewed']]
print(tabulate(data, headers=['Title', 'Date', 'Author', 'Status', 'Fidelity'], tablefmt='simple'))
"
```

Expected: Formatted table output

- [ ] **Step 3: Commit**

```bash
git add scripts/fetch-erpnext-blogs.py
git commit -m "feat: add rich status table output with tabulate"
```

---

## Task 8: Add JSON Summary Output

**Files:**

- Modify: `scripts/fetch-erpnext-blogs.py` (add output_json_summary function)

- [ ] **Step 1: Add output_json_summary function**

Add after `print_status_table` function in `scripts/fetch-erpnext-blogs.py`:

```python
def output_json_summary(results: list[dict]) -> None:
    """Output JSON summary to stdout for programmatic consumption."""
    summary = {
        'total': len(results),
        'new': sum(1 for r in results if r['status'] == 'new'),
        'unchanged': sum(1 for r in results if r['status'] == 'unchanged'),
        'updated': sum(1 for r in results if r['status'] == 'updated'),
        'errors': sum(1 for r in results if r['status'] == 'error'),
        'articles': results
    }
    print(json.dumps(summary))
```

- [ ] **Step 2: Commit**

```bash
git add scripts/fetch-erpnext-blogs.py
git commit -m "feat: add JSON summary output for programmatic use"
```

---

## Task 9: Rewrite Main Function

**Files:**

- Modify: `scripts/fetch-erpnext-blogs.py` (rewrite main to use new functions)

- [ ] **Step 1: Rewrite main function**

Replace the `main` function in `scripts/fetch-erpnext-blogs.py`:

```python
def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Sync blog articles from ERPNext with fidelity checking'
    )
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show what would happen without writing files')
    parser.add_argument('--list', '-l', action='store_true',
                        help='Only list available blogs, do not sync')
    parser.add_argument('--skip-images', action='store_true',
                        help='Skip downloading images')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show verbose output')
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    content_dir = script_dir.parent / 'content' / 'blog'

    if not content_dir.exists():
        print(f"Error: Content directory not found: {content_dir}", file=sys.stderr)
        sys.exit(2)

    print(f"Fetching blog list from {ERPNEXT_URL}...", file=sys.stderr)
    blogs = fetch_blog_list()

    if not blogs:
        print("No blogs found or error occurred.", file=sys.stderr)
        sys.exit(2)

    print(f"Found {len(blogs)} published blogs", file=sys.stderr)

    if args.list:
        # Just list the blogs
        results = []
        for blog in blogs:
            results.append({
                'title': blog.get('title', 'Untitled'),
                'date': str(blog.get('published_on', ''))[:10],
                'author': blog.get('blogger', 'Unknown'),
                'status': 'available',
                'fidelity': '-'
            })
        print_status_table(results, dry_run=True)
        return

    results = []
    errors_occurred = False

    for blog_summary in blogs:
        blog_name = blog_summary.get('name')
        if not blog_name:
            continue

        # Fetch full details
        blog = fetch_blog_detail(blog_name)
        if not blog:
            results.append({
                'title': blog_summary.get('title', 'Unknown'),
                'date': '-',
                'author': '-',
                'status': 'error',
                'fidelity': 'fetch failed'
            })
            errors_occurred = True
            continue

        # Sync the blog
        sync_result = sync_blog(blog, content_dir, dry_run=args.dry_run)

        results.append({
            'title': blog.get('title', 'Untitled'),
            'date': str(blog.get('published_on', ''))[:10],
            'author': blog.get('blogger', 'Unknown'),
            'status': sync_result['status'],
            'fidelity': sync_result['fidelity'],
            'file': sync_result.get('file', '')
        })

    # Output results
    print_status_table(results, dry_run=args.dry_run)
    output_json_summary(results)

    # Exit code based on errors
    if errors_occurred:
        sys.exit(1)
    sys.exit(0)
```

- [ ] **Step 2: Update docstring at top of file**

Replace the module docstring at the top of `scripts/fetch-erpnext-blogs.py`:

```python
#!/usr/bin/env python3
"""
Sync blog articles from ERPNext to Hugo with fidelity checking.

Features:
- Fetches all published blog articles from ERPNext
- Compares with local Hugo content (text-only, ignoring formatting)
- ERPNext is authoritative: overwrites local content when different
- Auto-marks articles as reviewed when fidelity check passes
- Outputs rich status table and JSON summary

Environment variables:
    ERPNEXT_URL: ERPNext instance URL (default: https://erp.kartoza.com)

Usage:
    ./fetch-erpnext-blogs.py              # Full sync with fidelity checking
    ./fetch-erpnext-blogs.py --dry-run    # Preview changes without writing
    ./fetch-erpnext-blogs.py --list       # List available blogs
    ./fetch-erpnext-blogs.py --verbose    # Verbose output
"""
```

- [ ] **Step 3: Remove unused imports and variables**

Remove these lines from the top of `scripts/fetch-erpnext-blogs.py`:

```python
# Remove these lines:
API_KEY = os.environ.get('ERPNEXT_API_KEY', '')
API_SECRET = os.environ.get('ERPNEXT_API_SECRET', '')
```

Update `get_auth_headers` to return empty dict (no auth needed for public blogs):

```python
def get_auth_headers() -> dict:
    """Get authentication headers for ERPNext API (empty for public blogs)."""
    return {}
```

- [ ] **Step 4: Run full test suite**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/test_fetch_erpnext_blogs.py -v
```

Expected: All tests PASS

- [ ] **Step 5: Manual integration test**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command ./scripts/fetch-erpnext-blogs.py --dry-run --list
```

Expected: List of blogs from ERPNext displayed in table format

- [ ] **Step 6: Commit**

```bash
git add scripts/fetch-erpnext-blogs.py
git commit -m "feat: rewrite main function with fidelity sync workflow"
```

---

## Task 10: Update sync-content-from-erpnext.py Integration

**Files:**

- Modify: `scripts/sync-content-from-erpnext.py:266-284` (update sync_blog_content method)

- [ ] **Step 1: Update sync_blog_content method**

Replace the `sync_blog_content` method in `scripts/sync-content-from-erpnext.py`:

```python
def sync_blog_content(self, download_images: bool = True) -> dict:
    """Sync blog articles by calling fetch-erpnext-blogs.py"""
    print("→ Syncing blog articles...")

    # Build command
    cmd = [sys.executable, str(PROJECT_ROOT / "scripts" / "fetch-erpnext-blogs.py")]
    if not download_images:
        cmd.append("--skip-images")

    # Run and capture output
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=os.environ,
        cwd=PROJECT_ROOT
    )

    # Print stderr (the status table) to console
    if result.stderr:
        print(result.stderr)

    # Parse JSON summary from stdout
    if result.stdout.strip():
        try:
            summary = json.loads(result.stdout.strip().split('\n')[-1])
            print(f"  ✓ Processed {summary['total']} articles: {summary['new']} new, {summary['unchanged']} unchanged, {summary['updated']} updated")
            return summary
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"  ✗ Error parsing sync output: {e}", file=sys.stderr)

    return {'total': 0, 'new': 0, 'unchanged': 0, 'updated': 0, 'errors': 0}
```

- [ ] **Step 2: Add subprocess import if missing**

Check top of `scripts/sync-content-from-erpnext.py` and add if not present:

```python
import subprocess
```

- [ ] **Step 3: Test integration**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command ./scripts/sync-content-from-erpnext.py --only blog --dry-run
```

Expected: Blog sync runs via subprocess, displays table and summary

- [ ] **Step 4: Commit**

```bash
git add scripts/sync-content-from-erpnext.py
git commit -m "feat: integrate fetch-erpnext-blogs.py via subprocess"
```

---

## Task 11: Final Integration Test

**Files:**

- None (testing only)

- [ ] **Step 1: Run full test suite**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command pytest scripts/tests/ -v
```

Expected: All tests PASS

- [ ] **Step 2: Run live sync (dry-run)**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command ./scripts/fetch-erpnext-blogs.py --dry-run
```

Expected: Table shows all ERPNext blogs with status (new/unchanged/updated)

- [ ] **Step 3: Run live sync (actual)**

```bash
cd /home/timlinux/dev/hugo/Kartoza-Hugo
nix develop --command ./scripts/fetch-erpnext-blogs.py
```

Expected: Files created/updated, articles marked as reviewed

- [ ] **Step 4: Verify Hugo renders the synced blogs**

Check: <http://localhost:1313/blog/> - should show newly reviewed articles

- [ ] **Step 5: Final commit**

```bash
git add -A
git status
# If any changes remaining:
git commit -m "chore: final cleanup after blog sync implementation"
```

---

## Summary

| Task | Description | Estimated Steps |
|------|-------------|-----------------|
| 1 | Add normalize_for_comparison | 6 |
| 2 | Add check_fidelity | 5 |
| 3 | Add read_local_blog | 5 |
| 4 | Add find_local_file | 5 |
| 5 | Update front matter with review fields | 5 |
| 6 | Implement sync_blog | 5 |
| 7 | Add rich status table | 3 |
| 8 | Add JSON summary output | 2 |
| 9 | Rewrite main function | 6 |
| 10 | Update sync-content-from-erpnext.py | 4 |
| 11 | Final integration test | 5 |

**Total: 11 tasks, ~51 steps**
