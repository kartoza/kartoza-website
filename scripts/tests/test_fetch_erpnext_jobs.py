#!/usr/bin/env python3
"""Tests for fetch-erpnext-jobs.py fidelity checking functions."""

import sys
from pathlib import Path
import tempfile
import os

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from importlib import import_module


def get_module():
    """Import the fetch script as a module."""
    spec = import_module('fetch-erpnext-jobs')
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
        assert "title first paragraph with link . item 1 item 2" == result


class TestCheckFidelity:
    """Tests for check_fidelity function."""

    def test_identical_content_returns_true(self):
        module = get_module()
        assert module.check_fidelity("Hello world", "Hello world") is True

    def test_different_content_returns_false(self):
        module = get_module()
        assert module.check_fidelity("Hello world", "Goodbye world") is False

    def test_ignores_html_formatting(self):
        module = get_module()
        local = "Hello world"
        remote = "<p>Hello <strong>world</strong></p>"
        assert module.check_fidelity(local, remote) is True

    def test_ignores_whitespace_differences(self):
        module = get_module()
        assert module.check_fidelity("Hello world", "Hello    \n\n   world") is True

    def test_ignores_case_differences(self):
        module = get_module()
        assert module.check_fidelity("hello world", "HELLO WORLD") is True

    def test_ignores_hugo_shortcodes(self):
        module = get_module()
        assert module.check_fidelity("Hello world", '{{< block >}}Hello world{{< /block >}}') is True


class TestReadLocalFile:
    """Tests for read_local_file function."""

    def test_reads_frontmatter_and_content(self):
        module = get_module()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("""---
title: "Test Job"
erpnext_id: "job-123"
---

This is the content.
""")
            f.flush()
            try:
                front_matter, content = module.read_local_file(Path(f.name))
                assert front_matter['title'] == "Test Job"
                assert front_matter['erpnext_id'] == "job-123"
                assert "This is the content." in content
            finally:
                os.unlink(f.name)

    def test_returns_none_for_missing_file(self):
        module = get_module()
        result = module.read_local_file(Path("/nonexistent/file.md"))
        assert result is None

    def test_handles_file_without_frontmatter(self):
        module = get_module()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("Just plain content without frontmatter.")
            f.flush()
            try:
                result = module.read_local_file(Path(f.name))
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
            (content_dir / "some-job.md").write_text("""---
title: "Some Job"
erpnext_id: "job-opening-123"
---
Content here.
""")
            result = module.find_local_file(content_dir, "job-opening-123", "Different Title")
            assert result is not None
            assert result.name == "some-job.md"

    def test_finds_by_slugified_title(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            (content_dir / "senior-developer.md").write_text("""---
title: "Senior Developer"
---
Content here.
""")
            result = module.find_local_file(content_dir, "unknown-id", "Senior Developer")
            assert result is not None
            assert result.name == "senior-developer.md"

    def test_returns_none_when_not_found(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            result = module.find_local_file(content_dir, "unknown", "Unknown Title")
            assert result is None

    def test_skips_index_files(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            (content_dir / "_index.md").write_text("""---
title: "Careers"
erpnext_id: "job-opening-123"
---
Index content.
""")
            result = module.find_local_file(content_dir, "job-opening-123", "Careers")
            assert result is None


class TestJobToHugoFrontmatter:
    """Tests for job_to_hugo_frontmatter function."""

    def test_includes_review_fields_when_requested(self):
        module = get_module()
        job = {
            'name': 'test-job',
            'job_title': 'Test Developer',
            'status': 'Open',
            'publish': 1,
            'creation': '2024-01-15 10:00:00',
            'modified': '2024-01-15 10:00:00',
        }
        result = module.job_to_hugo_frontmatter(job, mark_reviewed=True)
        assert result['reviewedBy'] == 'Automated Check'
        assert result['reviewedDate'] is not None
        assert len(result['reviewedDate']) == 10

    def test_excludes_review_fields_when_not_requested(self):
        module = get_module()
        job = {
            'name': 'test-job',
            'job_title': 'Test Developer',
            'status': 'Open',
            'publish': 1,
            'creation': '2024-01-15 10:00:00',
            'modified': '2024-01-15 10:00:00',
        }
        result = module.job_to_hugo_frontmatter(job, mark_reviewed=False)
        assert 'reviewedBy' not in result
        assert 'reviewedDate' not in result

    def test_marks_closed_job_as_draft(self):
        module = get_module()
        job = {
            'name': 'closed-job',
            'job_title': 'Closed Position',
            'status': 'Closed',
            'publish': 1,
            'creation': '2024-01-15 10:00:00',
        }
        result = module.job_to_hugo_frontmatter(job)
        assert result.get('draft') is True

    def test_marks_unpublished_job_as_draft(self):
        module = get_module()
        job = {
            'name': 'unpub-job',
            'job_title': 'Unpublished Position',
            'status': 'Open',
            'publish': 0,
            'creation': '2024-01-15 10:00:00',
        }
        result = module.job_to_hugo_frontmatter(job)
        assert result.get('draft') is True

    def test_includes_tags_from_metadata(self):
        module = get_module()
        job = {
            'name': 'tagged-job',
            'job_title': 'Developer',
            'designation': 'Senior Dev',
            'department': 'Engineering',
            'location': 'Cape Town',
            'creation': '2024-01-15 10:00:00',
        }
        result = module.job_to_hugo_frontmatter(job)
        assert 'Career' in result['tags']
        assert 'Senior Dev' in result['tags']
        assert 'Engineering' in result['tags']
        assert 'Cape Town' in result['tags']


class TestSyncJob:
    """Tests for sync_job function."""

    def test_creates_new_file(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            job = {
                'name': 'new-job',
                'job_title': 'New Developer Position',
                'description': '<p>This is a new job.</p>',
                'status': 'Open',
                'publish': 1,
                'creation': '2024-01-15 10:00:00',
                'modified': '2024-01-15 10:00:00',
            }
            result = module.sync_job(job, content_dir, dry_run=False)
            assert result['status'] == 'new'
            assert result['fidelity'] == 'auto-reviewed'
            assert (content_dir / 'new-developer-position.md').exists()

    def test_unchanged_when_fidelity_passes(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            # Create existing file with matching content (as markdown)
            (content_dir / 'existing-job.md').write_text("""---
title: "Existing Job"
erpnext_id: "existing-job"
reviewedBy: "Previous Reviewer"
reviewedDate: "2024-01-01"
---

This is the content.
""")
            job = {
                'name': 'existing-job',
                'job_title': 'Existing Job',
                'description': '<p>This is the content.</p>',
                'status': 'Open',
                'publish': 1,
                'creation': '2024-01-15 10:00:00',
                'modified': '2024-01-15 10:00:00',
            }
            result = module.sync_job(job, content_dir, dry_run=False)
            assert result['status'] == 'unchanged'
            assert result['fidelity'] == 'passed'

    def test_dry_run_does_not_write(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            job = {
                'name': 'dry-run-job',
                'job_title': 'Dry Run Position',
                'description': '<p>Content.</p>',
                'status': 'Open',
                'publish': 1,
                'creation': '2024-01-15 10:00:00',
                'modified': '2024-01-15 10:00:00',
            }
            result = module.sync_job(job, content_dir, dry_run=True)
            assert result['status'] == 'new'
            assert not (content_dir / 'dry-run-position.md').exists()

    def test_force_overwrites_existing(self):
        module = get_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            content_dir = Path(tmpdir)
            (content_dir / 'forced-job.md').write_text("""---
title: "Forced Job"
erpnext_id: "forced-job"
---

Old content.
""")
            job = {
                'name': 'forced-job',
                'job_title': 'Forced Job',
                'description': '<p>New content.</p>',
                'status': 'Open',
                'publish': 1,
                'creation': '2024-01-15 10:00:00',
                'modified': '2024-01-15 10:00:00',
            }
            result = module.sync_job(job, content_dir, force=True)
            assert result['status'] == 'forced'
            content = (content_dir / 'forced-job.md').read_text()
            assert 'New content' in content


class TestSlugify:
    """Tests for slugify function."""

    def test_basic_slugification(self):
        module = get_module()
        assert module.slugify("Hello World") == "hello-world"

    def test_removes_special_characters(self):
        module = get_module()
        assert module.slugify("Hello, World! (Test)") == "hello-world-test"

    def test_collapses_multiple_hyphens(self):
        module = get_module()
        assert module.slugify("Hello---World") == "hello-world"

    def test_strips_leading_trailing_hyphens(self):
        module = get_module()
        assert module.slugify("-Hello World-") == "hello-world"


class TestHtmlToMarkdown:
    """Tests for html_to_markdown function."""

    def test_converts_paragraph(self):
        module = get_module()
        result = module.html_to_markdown("<p>Hello world</p>")
        assert "Hello world" in result

    def test_converts_list(self):
        module = get_module()
        result = module.html_to_markdown("<ul><li>Item 1</li><li>Item 2</li></ul>")
        assert "Item 1" in result
        assert "Item 2" in result

    def test_empty_input(self):
        module = get_module()
        assert module.html_to_markdown("") == ""

    def test_none_input(self):
        module = get_module()
        assert module.html_to_markdown(None) == ""
