#!/usr/bin/env python3
"""Tests for fetch-erpnext-blogs.py fidelity checking functions."""

import sys
from pathlib import Path
import tempfile
import os

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
        # Note: BeautifulSoup's get_text(separator=' ') adds space between elements
        # so "link</a>." becomes "link ." - this is expected for text extraction
        assert "title first paragraph with link . item 1 item 2" == result


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
        assert result['reviewedDate'] is not None
        # Just verify it's in ISO date format (YYYY-MM-DD)
        assert len(result['reviewedDate']) == 10
        assert result['reviewedDate'].count('-') == 2

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
