#!/usr/bin/env python3
"""
Sync blog articles from ERPNext to Hugo with fidelity checking.

Features:
- Fetches all blog articles from the ERPNext REST API; unpublished ones
  become Hugo drafts, but only when they already exist locally
- Compares with local Hugo content (text-only, ignoring formatting)
- ERPNext is authoritative: overwrites local content when different
- Auto-marks articles as reviewed when fidelity check passes
- Outputs rich status table and JSON summary

Environment variables:
    ERPNEXT_URL: ERPNext instance URL (default: https://erp.kartoza.com)
    ERPNEXT_API_KEY, ERPNEXT_API_SECRET: API credentials (required)

Usage:
    ./fetch-erpnext-blogs.py              # Full sync with fidelity checking
    ./fetch-erpnext-blogs.py --dry-run    # Preview changes without writing
    ./fetch-erpnext-blogs.py --list       # List available blogs
    ./fetch-erpnext-blogs.py --verbose    # Verbose output
"""

import html
import html2text
import json
import re
import requests
import sys
import warnings
import yaml
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
from datetime import datetime
from dateutil import parser as date_parser
from pathlib import Path
from tabulate import tabulate

from fetch_erpnext_client import ERPNextClient
from fetch_erpnext_utilities import (
    check_fidelity,
    find_local_file,
    normalize_for_comparison,
    read_local_file,
    slugify,
    update_review_fields,
)

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Configuration
ERPNEXT = ERPNextClient()
KARTOZA_URL = 'https://kartoza.com'

# Image storage path relative to Hugo static folder
IMAGE_DIR = 'img/blog/erpnext'

PLACEHOLDER_IMAGE = '/img/blog/placeholder.png'
# Placeholder paths that mean the post has no image of its own; the
# second is a copy older syncs downloaded by mistake
PLACEHOLDER_IMAGES = (PLACEHOLDER_IMAGE, f'/{IMAGE_DIR}/placeholder.png')


def download_image(
        url: str, static_dir: Path, verbose: bool = False
) -> str | None:
    """
    Download an image from ERPNext and save it locally.

    Args:
        url: The image URL (can be relative like /files/xxx or absolute)
        static_dir: Path to Hugo's static directory

    Returns:
        Local path to use in markdown
        (e.g., /img/blog/erpnext/xxx.png) or None on failure
    """
    # Site paths that already exist, like the placeholder, stay as they are
    if (url.startswith('/') and not url.startswith(('/files/', '/private/'))
            and (static_dir / url.lstrip('/')).exists()):
        return url

    # Normalize the URL
    if url.startswith('/private/files/'):
        # Private files need auth, so fetch them from ERPNext directly
        full_url = f"{ERPNEXT.base_url}{url}"
        filename = url.split('/')[-1]
    elif url.startswith('/files/'):
        full_url = f"{KARTOZA_URL}{url}"
        filename = url.split('/')[-1]
    elif url.startswith('/'):
        full_url = f"{KARTOZA_URL}{url}"
        filename = url.split('/')[-1]
    elif re.search(r'kartoza\.erpnext\.com/(private/)?files/', url):
        # The old ERPNext host is gone, the files now live on ERPNext
        path = re.sub(r'^https?://kartoza\.erpnext\.com', '', url)
        full_url = f"{ERPNEXT.base_url}{path}"
        filename = url.split('/')[-1]
    elif re.search(r'kartoza\.com/(private/)?files/', url):
        full_url = url
        filename = url.split('/')[-1]
    else:
        # Not a Kartoza image, leave as-is
        return None

    # Create target directory
    target_dir = static_dir / IMAGE_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / filename
    local_url = f"/{IMAGE_DIR}/{filename}"

    # Skip if already downloaded
    if target_path.exists():
        return local_url

    # Download the image
    try:
        if verbose:
            print(f"  Downloading: {filename}", file=sys.stderr)
        response = ERPNEXT.get(full_url)
        response.raise_for_status()
        target_path.write_bytes(response.content)
        return local_url
    except requests.RequestException as e:
        print(
            f"  Warning: Failed to download {full_url}: {e}",
            file=sys.stderr
        )
        return None


def process_images_in_content(
        content: str, static_dir: Path, verbose: bool = False
) -> str:
    """
    Find all images in markdown content, download them, and rewrite URLs.

    Args:
        content: Markdown content with image references
        static_dir: Path to Hugo's static directory

    Returns:
        Content with rewritten image URLs
    """
    # Pattern for markdown images: ![alt](/files/xxx) or
    # ![alt](https://kartoza.com/files/xxx)
    img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

    def replace_image(match):
        alt_text = match.group(1)
        img_url = match.group(2)

        # Try to download and get local path
        local_path = download_image(img_url, static_dir, verbose=verbose)

        if local_path:
            return f'![{alt_text}]({local_path})'
        else:
            # Keep original URL if download failed or not a Kartoza image
            return match.group(0)

    return img_pattern.sub(replace_image, content)


def process_thumbnail(
        thumbnail_url: str, static_dir: Path, verbose: bool = False
) -> str:
    """
    Download thumbnail image and return local path.

    Args:
        thumbnail_url: The thumbnail URL
        static_dir: Path to Hugo's static directory

    Returns:
        Local path or original URL if download failed
    """
    if not thumbnail_url:
        return PLACEHOLDER_IMAGE

    local_path = download_image(thumbnail_url, static_dir, verbose=verbose)
    return local_path if local_path else thumbnail_url


def sync_blog(
        blog: dict, content_dir: Path, static_dir: Path, dry_run: bool = False,
        force: bool = False, skip_images: bool = False, verbose: bool = False
) -> dict:
    """
    Sync a single blog article from ERPNext to Hugo.

    Performs fidelity checking and updates review fields.

    Args:
        blog: Blog data from ERPNext
        content_dir: Path to Hugo content directory
        static_dir: Path to Hugo static directory (for images)
        dry_run: If True, don't write files
        force: If True, overwrite all files regardless of fidelity
        skip_images: If True, don't download images
        verbose: If True, show detailed output

    Returns:
        Dict with 'status' and 'fidelity' keys
    """
    erpnext_id = blog.get('name', '')
    title = blog.get('title', 'Untitled')
    erpnext_content = get_blog_content(blog)

    # Find existing local file
    local_file = find_local_file(content_dir, erpnext_id, title)
    result = read_local_file(local_file) if local_file else None

    if local_file and not force:
        # File exists - check fidelity (skip if force mode)
        if result:
            local_frontmatter, local_content = result
            # A change of published state always needs a rewrite
            same_draft = (
                bool(local_frontmatter.get('draft')) == bool(blog.get('draft'))
            )
            if same_draft and check_fidelity(local_content, erpnext_content):
                # Content matches - fidelity passed
                # Update review fields if not already set
                if not local_frontmatter.get('reviewedBy'):
                    if not dry_run:
                        update_review_fields(
                            local_file, local_frontmatter, local_content
                        )
                return {'status': 'unchanged', 'fidelity': 'passed',
                        'file': local_file.name}

        # Content differs - overwrite with ERPNext
        status = 'updated'
        filepath = local_file
    elif local_file and force:
        # Force mode - overwrite existing file
        status = 'forced'
        filepath = local_file
    elif blog.get('draft'):
        # Unpublished and not on the site yet, so nothing to add
        return {'status': 'skipped', 'fidelity': '-', 'file': ''}
    else:
        # New file
        status = 'new'
        slug = slugify(title)
        filepath = content_dir / f"{slug}.md"

    # Generate content
    front_matter = blog_to_hugo_frontmatter(blog, mark_reviewed=True)
    content = blog_to_hugo_content(blog)

    # Process images (download and rewrite URLs)
    if not skip_images and not dry_run:
        content = process_images_in_content(
            content, static_dir, verbose=verbose
        )
        # Also process thumbnail
        if front_matter.get('thumbnail'):
            front_matter['thumbnail'] = process_thumbnail(
                front_matter['thumbnail'], static_dir, verbose=verbose
            )

    if result:
        local_frontmatter, local_content = result

        # Descriptions are often written by hand locally, so keep the local
        # one, unless it is a cut-off part of the ERPNext one or broken HTML
        local_description = str(local_frontmatter.get('description') or '')
        erpnext_description = front_matter.get('description') or ''
        # A full sentence was finished by hand, so it is not cut off
        local_is_cut = (
            not re.search(r'[.!?…"\')’”]$', local_description.strip())
            and comparable_description(local_description)
            in comparable_description(erpnext_description)
            and len(erpnext_description) > len(local_description)
        )
        if (local_description and '<' not in local_description
                and not local_is_cut):
            front_matter['description'] = local_description

        # Keep the local thumbnail when ERPNext has no image for the post
        local_thumbnail = local_frontmatter.get('thumbnail')
        if (front_matter.get('thumbnail') in PLACEHOLDER_IMAGES
                and local_thumbnail
                and local_thumbnail not in PLACEHOLDER_IMAGES):
            front_matter['thumbnail'] = local_thumbnail

        # Keep the previous review fields if the content itself did not change
        if (local_frontmatter.get('reviewedDate')
                and comparable_text(local_content) ==
                comparable_text(content)):
            for field in ('reviewedBy', 'reviewedDate'):
                if local_frontmatter.get(field):
                    front_matter[field] = local_frontmatter[field]

    # Build file content
    file_content = "---\n"
    file_content += yaml.dump(
        front_matter, default_flow_style=False, allow_unicode=True
    )
    file_content += "---\n\n"
    file_content += content
    file_content += "\n"

    if not dry_run:
        filepath.write_text(file_content)

    return {
        'status': status, 'fidelity': 'auto-reviewed', 'file': filepath.name
    }


def comparable_description(text: str) -> str:
    """Normalize a description: quotes, whitespace and case."""
    text = text.replace('’', "'").replace('‘', "'")
    text = text.replace('“', '"').replace('”', '"')
    return ' '.join(text.split()).lower()


def comparable_text(markdown: str) -> str:
    """Normalize markdown so cleanup-only changes don't count as changes.

    Applies the same cleanup as new content, and ignores code fences, which
    older content had as indented code blocks.
    """
    markdown = clean_markdown(fix_list_markers(markdown))
    markdown = re.sub(r'^\s*```.*$', '', markdown, flags=re.MULTILINE)
    # Ignore table pipes and separator rows, as older content had no padding
    markdown = re.sub(r'^[\s|:-]*-{3,}[\s|:-]*$', '', markdown, flags=re.MULTILINE)
    markdown = markdown.replace('|', ' ')
    return normalize_for_comparison(markdown)


def fetch_blogger_name(blogger: str) -> str:
    """Fetch a blogger's full name, falling back to the blogger ID."""
    try:
        response = ERPNEXT.get(
            f"{ERPNEXT.base_url}/api/resource/Blogger/{blogger}"
        )
        response.raise_for_status()
        return response.json().get('data', {}).get('full_name') or blogger
    except (requests.RequestException, json.JSONDecodeError):
        return blogger


def find_first_image(post: dict) -> str:
    """Find the first image URL in a blog post's content.

    This is what the public blog list uses as cover image.
    """
    content = get_blog_content(post)
    if post.get('content_type') == 'Markdown':
        match = re.search(r'!\[[^\]]*\]\(<?([^)>\s]+)', content)
        return match.group(1) if match else ''

    img = BeautifulSoup(content, 'html.parser').find('img', src=True)
    return img['src'] if img else ''


def fetch_blogs() -> list[dict]:
    """Fetch all blog posts, with their content, using the REST API.

    The REST API has the source of every post: the Markdown of Markdown
    posts, which the public page renders badly, and the full blog intro,
    which the page's meta description cuts at 140 characters. Unpublished
    posts are synced as Hugo drafts.
    """
    fields = [
        'name', 'title', 'route', 'published', 'blogger', 'blog_category',
        'published_on', 'creation', 'blog_intro', 'meta_image',
        'content_type', 'content', 'content_md', 'content_html',
    ]
    try:
        response = ERPNEXT.get(
            f"{ERPNEXT.base_url}/api/resource/Blog Post",
            params={
                'fields': json.dumps(fields),
                'order_by': 'published_on desc',
                'limit_page_length': 0,
            }
        )
        response.raise_for_status()
        posts = response.json().get('data', [])
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching blogs: {e}", file=sys.stderr)
        return []

    blogger_names = {}
    blogs = []
    for post in posts:
        category = post.get('blog_category') or 'uncategorised'
        route = post.get('route') or f"blog/{category}/{post['name']}"
        # The category tag comes from the URL path, like the site's URLs
        parts = route.strip('/').split('/')
        if len(parts) >= 3:
            category = parts[1]

        blogger = post.get('blogger') or 'Kartoza'
        if blogger not in blogger_names:
            blogger_names[blogger] = fetch_blogger_name(blogger)

        published_on = post.get('published_on') or post.get('creation') or ''
        blogs.append({
            'name': f"/{route.strip('/')}",
            # Collapse stray whitespace, newlines and &nbsp; from the editor
            'title': ' '.join(
                html.unescape(post.get('title') or '').split()
            ) or 'Untitled',
            'blog_intro': ' '.join(
                html.unescape(post.get('blog_intro') or '').split()
            ),
            'blogger': blogger_names[blogger],
            'published_on': published_on,
            'modified': published_on,  # Use published date as modified
            'blog_category': category,
            'content_type': post.get('content_type'),
            'content': post.get('content') or '',
            'content_md': post.get('content_md') or '',
            'content_html': post.get('content_html') or '',
            # The public list uses the first image in the content as cover
            'featured_image': (
                post.get('meta_image') or find_first_image(post)
            ),
            'draft': not post.get('published'),
        })

    return blogs


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

    # Get thumbnail from featured_image or use placeholder
    thumbnail = blog.get('featured_image', '') or PLACEHOLDER_IMAGE
    # Ensure full URL for external images
    if thumbnail and not thumbnail.startswith(('http://', 'https://', '/')):
        thumbnail = f"{ERPNEXT.base_url}/{thumbnail}"

    # Build front matter
    front_matter = {
        'title': blog.get('title', 'Untitled'),
        'description': blog.get('blog_intro', '')[:500] if blog.get(
            'blog_intro') else '',
        'date': date_str,
        'author': blog.get('blogger', 'Kartoza'),
        'thumbnail': thumbnail,
        'tags': [],
        'erpnext_id': blog.get('name', ''),
        'erpnext_modified': blog.get('modified', ''),
    }

    # Add category as tag (capitalize first letter)
    if blog.get('blog_category'):
        category = blog['blog_category']
        # Capitalize first letter of each word
        category = category.replace('-', ' ').title()
        front_matter['tags'].append(category)

    # Unpublished in ERPNext
    if blog.get('draft'):
        front_matter['draft'] = True

    # Add review fields if requested
    if mark_reviewed:
        front_matter['reviewedBy'] = 'Automated Check'
        front_matter['reviewedDate'] = datetime.now().strftime('%Y-%m-%d')

    return front_matter


def get_blog_content(blog: dict) -> str:
    """Get the blog content from the field matching its content type."""
    if blog.get('content_type') == 'Markdown':
        return blog.get('content_md') or ''
    if blog.get('content_type') == 'HTML':
        return blog.get('content_html') or ''
    return blog.get('content') or blog.get('content_html') or ''


def blog_to_hugo_content(blog: dict) -> str:
    """Convert ERPNext blog content to Hugo markdown using html2text."""
    content = get_blog_content(blog)

    if not content:
        return ''

    # Markdown posts from the API need no conversion
    if blog.get('content_type') == 'Markdown':
        return clean_markdown(content)

    # Configure html2text for clean markdown output
    h = html2text.HTML2Text()
    h.body_width = 0  # Don't wrap lines
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.skip_internal_links = False
    h.inline_links = True
    h.protect_links = True
    h.unicode_snob = True  # Use unicode instead of ASCII
    # Tables with full pipes; without them a one-column table reads as a
    # setext heading (MD003, MD022)
    h.pad_tables = True

    # Take code blocks out first, so html2text and the list fixes can't
    # mangle them
    html, code_blocks = extract_code_blocks(
        fix_inline_formatting(
            fix_quill_blockquotes(fix_quill_lists(fix_split_lists(content)))
        )
    )

    # Convert HTML to markdown
    markdown = fix_list_markers(h.handle(html))

    return clean_markdown(
        nest_code_in_lists(restore_code_blocks(markdown, code_blocks))
    )


def nest_code_in_lists(markdown: str) -> str:
    """Indent code blocks between numbered steps into the step above.

    A code block at the left margin ends a list, so the next step starts a
    new list at "2." or "6.", which markdownlint rejects (MD029). Indented,
    the code belongs to the step above and the steps stay one list.
    """
    lines = markdown.split('\n')
    result = []
    i = 0
    last_item = None  # (number, content indent) of the last top-level step
    while i < len(lines):
        line = lines[i]
        item = re.match(r'(\d+)[.)]( +)', line)
        if item:
            last_item = (int(item.group(1)), len(item.group(0)))
        elif line.startswith('```') and last_item:
            # Find the end of the code block and the next non-blank line
            end = i + 1
            while end < len(lines) and not lines[end].startswith('```'):
                end += 1
            following = end + 1
            while following < len(lines) and not lines[following].strip():
                following += 1
            next_item = (
                re.match(r'(\d+)[.)] ', lines[following])
                if following < len(lines) else None
            )
            if (end < len(lines) and next_item
                    and int(next_item.group(1)) == last_item[0] + 1):
                indent = ' ' * last_item[1]
                result.extend(
                    indent + code_line if code_line else code_line
                    for code_line in lines[i:end + 1]
                )
                i = end + 1
                continue
        elif line.strip() and not line.startswith(' '):
            last_item = None  # Text at the left margin ends the list
        result.append(line)
        i += 1

    return '\n'.join(result)


CODE_BLOCK_PLACEHOLDER = 'KARTOZACODEBLOCK'


def extract_code_blocks(html: str) -> tuple[str, list[str]]:
    """Replace <pre> blocks with placeholders and render them as fenced code.

    Quill stores each code line as a <div class="ql-code-block"> and indents
    with non-breaking spaces, which html2text turns into code with a blank
    line after every line.
    """
    soup = BeautifulSoup(html, 'html.parser')
    code_blocks = []

    # Multi-line inline code that is a paragraph of its own is really a code
    # block; html2text would turn it into inline code spanning lines (MD038)
    for code in soup.find_all('code'):
        parent = code.parent
        if code.find_parent('pre') or not code.find('br') or parent is None:
            continue
        others = [
            child for child in parent.contents
            if child is not code and (not isinstance(child, str) or child.strip())
        ]
        if parent.name not in ('p', 'div') or others:
            continue
        for br in code.find_all('br'):
            br.replace_with('\n')
        text = code.get_text()

        # Pieces in paragraphs that follow each other form one code block
        previous = parent.previous_sibling
        while isinstance(previous, str) and not previous.strip():
            previous = previous.previous_sibling
        if getattr(previous, 'name', None) == 'pre' and previous.get(
                'data-from-code'):
            previous.string = previous.get_text() + '\n' + text
            parent.decompose()
        else:
            pre = soup.new_tag('pre', attrs={'data-from-code': '1'})
            pre.string = text
            parent.replace_with(pre)

    for pre in soup.find_all('pre'):
        quill_lines = pre.select('div.ql-code-block')
        if quill_lines:
            lines = [div.get_text() for div in quill_lines]
            language = quill_lines[0].get('data-language', '')
        else:
            # get_text() drops <br>, which some code blocks use as newlines
            for br in pre.find_all('br'):
                br.replace_with('\n')
            lines = pre.get_text().split('\n')
            language = ''
        if language == 'plain':
            language = ''

        code = '\n'.join(lines).replace('\xa0', ' ').strip('\n')
        code_blocks.append(f'```{language}\n{code}\n```')

        placeholder = soup.new_tag('p')
        placeholder.string = f'{CODE_BLOCK_PLACEHOLDER}{len(code_blocks) - 1}'
        pre.replace_with(placeholder)

    return str(soup), code_blocks


def restore_code_blocks(markdown: str, code_blocks: list[str]) -> str:
    """Put the code blocks taken out by extract_code_blocks back.

    The placeholder's prefix, which is the indent and any blockquote
    markers, is repeated on every line of the code block.
    """
    def restore(match):
        prefix = match.group(1)
        code = code_blocks[int(match.group(2))]
        return '\n'.join(
            prefix + line if line else prefix.rstrip()
            for line in code.split('\n')
        )

    return re.sub(
        rf'^([ >]*){CODE_BLOCK_PLACEHOLDER}(\d+)$', restore, markdown,
        flags=re.MULTILINE
    )


def fix_list_markers(markdown: str) -> str:
    """Fix html2text list output for markdownlint (MD004, MD007).

    html2text indents every list item by two extra spaces and uses "*"
    bullets; markdownlint wants "-" bullets starting at the left margin.
    The markdown must not contain code blocks, as code lines can look like
    list items.
    """
    lines = []
    for line in markdown.split('\n'):
        if re.match(
                rf' {{2}}\s*(?:[-*+] |\d+\. |{CODE_BLOCK_PLACEHOLDER})', line
        ):
            line = line[2:]
        # Leave "* * *" horizontal rules alone
        if not re.fullmatch(r'\*( \*)+', line.strip()):
            line = re.sub(r'^(\s*)[*+](?= )', r'\1-', line)
        lines.append(line)

    return '\n'.join(lines)


def fix_split_lists(html: str) -> str:
    """Join lists that the editor split up, and drop empty paragraphs.

    Some posts have every item in its own list wrapped in a second list,
    like <ul><ul><li>, with empty paragraphs between them. html2text then
    indents every item (MD007) and restarts every numbered item at 1.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Empty paragraphs only add blank lines: <p></p>, <p><br>&nbsp;</p>
    for paragraph in soup.find_all('p'):
        if (not paragraph.get_text().replace('\xa0', '').strip()
                and not paragraph.find(['img', 'iframe', 'video'])):
            paragraph.decompose()

    # A list holding nothing but lists is unwrapped: <ul><ul><li>
    unwrapped = True
    while unwrapped:
        unwrapped = False
        for outer in soup.find_all(['ul', 'ol']):
            children = [
                child for child in outer.children
                if not isinstance(child, str) or child.strip()
            ]
            if children and all(
                    getattr(child, 'name', None) in ('ul', 'ol')
                    for child in children):
                outer.unwrap()
                unwrapped = True
                break

    # Lists of the same kind next to each other are one list
    for current in soup.find_all(['ul', 'ol']):
        if current.parent is None:
            continue  # Already merged into the previous one
        following = current.next_sibling
        while following is not None:
            if isinstance(following, str) and not following.strip():
                following = following.next_sibling
                continue
            if getattr(following, 'name', None) != current.name:
                break
            for item in list(following.children):
                current.append(item.extract())
            next_sibling = following.next_sibling
            following.decompose()
            following = next_sibling

    return str(soup)


INLINE_TAGS = ['code', 'strong', 'b', 'em', 'i']


def fix_inline_formatting(html: str) -> str:
    """Tidy inline code and emphasis that older editors left messy.

    Pasted posts split one piece of code over several <code> tags inside
    <span>s, and have emphasis around only spaces or punctuation, or with
    spaces inside it. html2text turns these into "`a``b`", "_._" or
    "** text**" (MD037, MD038).
    """
    soup = BeautifulSoup(html, 'html.parser')

    def outside_pre(tags):
        return [tag for tag in tags if not tag.find_parent('pre')]

    # Spans and fonts only carry styling, which markdown can't keep
    for tag in outside_pre(soup.find_all(['span', 'font'])):
        tag.unwrap()
    soup = BeautifulSoup(str(soup), 'html.parser')  # Join the split strings

    # Emphasis around nothing but spaces or punctuation is no emphasis, and
    # code around nothing but spaces or a <br> is no code
    for tag in outside_pre(soup.find_all(['strong', 'b', 'em', 'i'])):
        if tag.parent is not None and not re.search(r'\w', tag.get_text()):
            tag.unwrap()
    for tag in outside_pre(soup.find_all('code')):
        # A <br> at the end of inline code would break it over two lines
        for br in reversed(tag.find_all('br')):
            after = ''.join(
                text for text in br.find_all_next(string=True)
                if tag in text.parents
            )
            if after.strip():
                break
            br.decompose()
        if tag.parent is not None and not tag.get_text().strip():
            tag.unwrap()

    # A markdown table row is one line, so table cells can't break lines
    for cell in soup.find_all(['td', 'th']):
        for br in cell.find_all('br'):
            br.replace_with(' ')
        for paragraph in cell.find_all('p'):
            paragraph.insert_after(' ')
            paragraph.unwrap()

    # A <br> at the end of a paragraph or list item breaks nothing
    for br in outside_pre(soup.find_all('br')):
        rest = br.next_siblings
        if br.parent is not None and br.parent.name in ('p', 'li') and not any(
                not isinstance(sibling, str) or sibling.strip()
                for sibling in rest):
            br.decompose()

    # The same tags right next to each other are one: <code>a</code><code>b
    for tag in outside_pre(soup.find_all(INLINE_TAGS)):
        if tag.parent is None:
            continue
        following = tag.next_sibling
        while getattr(following, 'name', None) == tag.name:
            for child in list(following.children):
                tag.append(child.extract())
            following.decompose()
            following = tag.next_sibling

    # Spaces at the edges go outside: <strong>Note: </strong> -> **Note:**
    # Innermost first, so a space moved out of an <em> also leaves the
    # <strong> around it
    for tag in reversed(outside_pre(soup.find_all(INLINE_TAGS))):
        if tag.parent is None or not tag.get_text().strip():
            continue
        first = tag.contents[0]
        if isinstance(first, str) and first != first.lstrip():
            first.replace_with(first.lstrip())
            tag.insert_before(' ')
        last = tag.contents[-1]
        if isinstance(last, str) and last != last.rstrip():
            last.replace_with(last.rstrip())
            tag.insert_after(' ')

    return str(soup)


def fix_quill_blockquotes(html: str) -> str:
    """Merge Quill's one-line blockquotes into one blockquote.

    Quill stores every line of a quote as its own <blockquote>, which
    html2text renders as separate quotes with blank lines between them
    (MD028).
    """
    soup = BeautifulSoup(html, 'html.parser')

    def next_blockquote(element):
        """The next sibling if it is a blockquote with only whitespace between."""
        sibling = element.next_sibling
        while isinstance(sibling, str) and not sibling.strip():
            sibling = sibling.next_sibling
        if getattr(sibling, 'name', None) == 'blockquote':
            return sibling
        return None

    for blockquote in soup.find_all('blockquote'):
        if blockquote.parent is None:
            continue  # Already merged into the previous one
        following = next_blockquote(blockquote)
        while following is not None:
            blockquote.append(soup.new_tag('br'))
            for child in list(following.children):
                blockquote.append(child.extract())
            following.decompose()
            following = next_blockquote(blockquote)

    return str(soup)


def fix_quill_lists(html: str) -> str:
    """Convert Quill's flat lists into nested HTML lists.

    Quill stores every list as a flat <ol>, with the list type in the
    data-list attribute and the nesting level in a ql-indent-N class.
    html2text does not know these, so it renders a flat numbered list.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Quill UI helpers, not content
    for ui in soup.select('span.ql-ui'):
        ui.decompose()

    for quill_list in soup.find_all(['ol', 'ul']):
        items = quill_list.find_all('li', recursive=False)
        if not any(li.has_attr('data-list') for li in items):
            continue

        roots = []
        stack = []  # (level, list tag) from outermost to innermost
        for li in items:
            level = 0
            for cls in li.get('class', []):
                match = re.fullmatch(r'ql-indent-(\d+)', cls)
                if match:
                    level = int(match.group(1))
            tag = 'ol' if li.get('data-list') == 'ordered' else 'ul'
            del li['data-list']
            li['class'] = [
                cls for cls in li.get('class', [])
                if not cls.startswith('ql-indent-')
            ]

            # Close deeper lists, and a same-level list of another type
            while stack and stack[-1][0] > level:
                stack.pop()
            if stack and stack[-1][0] == level and stack[-1][1].name != tag:
                stack.pop()

            if not stack or stack[-1][0] < level:
                new_list = soup.new_tag(tag)
                if stack:
                    stack[-1][1].find_all('li', recursive=False)[-1].append(
                        new_list
                    )
                else:
                    roots.append(new_list)
                stack.append((level, new_list))

            stack[-1][1].append(li.extract())

        quill_list.replace_with(*roots)

    # Quill keeps counting ordered lists that are only split by code blocks
    for ordered_list in soup.find_all('ol'):
        previous = ordered_list.find_previous_sibling()
        while previous is not None and previous.name == 'pre':
            previous = previous.find_previous_sibling()
        if previous is not None and previous.name == 'ol':
            start = int(previous.get('start', 1))
            count = len(previous.find_all('li', recursive=False))
            ordered_list['start'] = str(start + count)

    return str(soup)


def trim_code_span(match: re.Match, line: str) -> str:
    """Trim an inline code span, keeping a space to separate it from words."""
    before = line[match.start() - 1] if match.start() > 0 else ' '
    after = line[match.end()] if match.end() < len(line) else ' '
    lead = ' ' if match.group(1) and before.isalnum() else ''
    trail = ' ' if match.group(3) and after.isalnum() else ''
    return f'{lead}`{match.group(2)}`{trail}'


def wrap_bare_urls(line: str) -> str:
    """Turn bare URLs into autolinks: "see https://x.org." -> "see <https://x.org>." (MD034).

    Inline code, markdown links and existing autolinks are left alone.
    """
    def wrap(match):
        url = match.group(0)
        # Sentence punctuation after a URL is not part of it
        trailing = re.search(r'[.,;:!?]+$', url)
        if trailing:
            url, rest = url[:trailing.start()], trailing.group(0)
        else:
            rest = ''
        if url.endswith(')') and '(' not in url:
            url, rest = url[:-1], ')' + rest
        return f'<{url}>{rest}'

    parts = re.split(r'(`[^`]*`|!?\[[^\]]*\]\([^)]*\)|<[^>\s]+>)', line)
    return ''.join(
        part if i % 2 else re.sub(r'https?://[^\s<>`"\]]+', wrap, part)
        for i, part in enumerate(parts)
    )


def clean_markdown(markdown: str) -> str:
    """Clean up markdown so the output passes markdownlint.

    Drops zero-width characters, empty headings and trailing whitespace,
    collapses multiple blank lines (MD009, MD012), and makes links to
    kartoza.com relative.
    """
    # Zero-width characters usually come from copy-pasting into ERPNext
    markdown = re.sub(r'[​‌‍﻿]', '', markdown)

    # https://www.kartoza.com/en/page/ -> /en/page/
    markdown = re.sub(
        r'(\]\(<?)https?://(?:www\.)?kartoza\.com(?![\w.-])/?', r'\1/',
        markdown
    )

    # Move spaces out of link text: "[ here ](url)" -> " [here](url) " (MD039)
    markdown = re.sub(
        r'(?<!!)\[( *)([^\]\n]*?)( *)\]\(([^)\n]*)\)',
        r'\1[\2](\4)\3', markdown
    )

    lines = []
    in_code_block = False
    # (original level, new level) of the enclosing headings
    heading_stack = []
    # Next number of the open ordered lists, by indent
    list_numbers = {}
    # Whether the previous line was a heading, which needs a blank line below
    after_heading = False
    for line in markdown.split('\n'):
        stripped = line.rstrip()
        if stripped.lstrip().startswith(('```', '~~~')):
            in_code_block = not in_code_block
        # Drop empty headings like "###", but not "#" comments in code
        if not in_code_block and re.fullmatch(r'#{1,6}', stripped):
            continue
        # Headings may only go one level deeper at a time (MD001). The page
        # title is the h1, so the first heading can be at most an h2.
        heading = re.match(r'(#{1,6})(\s.*)$', stripped)
        if not in_code_block and heading:
            level = len(heading.group(1))
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            parent_level = heading_stack[-1][1] if heading_stack else 1
            new_level = min(level, parent_level + 1)
            heading_stack.append((level, new_level))
            # No trailing punctuation like "Overview:" (MD026); "?" is fine
            text = re.sub(r'\\?[.,;:!。，；：！]+$', '', heading.group(2).rstrip())
            stripped = '#' * new_level + (text if text.strip() else heading.group(2))
        # Number ordered list items in sequence, from the first item's number
        # (MD029). Markdown renders them in sequence anyway, so typos like a
        # repeated "4)" don't change the page.
        if not in_code_block and stripped:
            indent = len(stripped) - len(stripped.lstrip(' '))
            item = re.match(r'( *)(\d+)([.)]\s.*)$', stripped)
            bullet = re.match(r' *[-*+]\s', stripped)
            for open_indent in list(list_numbers):
                # Deeper lists end at any line that is not deeper still,
                # and a list ends at text or a bullet at its own indent
                if (open_indent > indent
                        or open_indent == indent and not item):
                    del list_numbers[open_indent]
            if item:
                number = list_numbers.get(indent, int(item.group(2)))
                list_numbers[indent] = number + 1
                stripped = f'{item.group(1)}{number}{item.group(3)}'
            elif not bullet and indent == 0:
                list_numbers.clear()
        if not in_code_block:
            # One space after a blockquote ">" (MD027): "> text", not
            # ">  text". Nested list items in a quote keep their indent.
            stripped = re.sub(
                r'^((?:> ?)*>) {2,}(?![-*+] |\d+[.)] )(?=\S)', r'\1 ',
                stripped
            )
            # "*" and "+" bullets become "-" (MD004), but not "* * *" rules
            if not re.fullmatch(r'\*( \*)+', stripped.strip()):
                stripped = re.sub(r'^(\s*)[*+](?= )', r'\1-', stripped)
            # A list right below a sentence needs a blank line before it
            # (MD032). Only "-" and "1." lists, as other numbers can't start
            # a list there and would change the page.
            previous = lines[-1] if lines else ''
            if (re.match(r'(- |1[.)] )', stripped) and previous.strip()
                    and not previous.startswith((' ', '>'))
                    and not re.match(r'([-*+]|\d+[.)]) ', previous)):
                lines.append('')
            stripped = wrap_bare_urls(stripped)
        # Drop spaces inside inline code: "a ` code `." -> "a `code`." (MD038)
        if not in_code_block and '``' not in stripped:
            stripped = re.sub(
                r'`( *)([^`\n]*?[^ `\n])( *)`',
                lambda match: trim_code_span(match, stripped), stripped
            )
        # Headings need blank lines above and below them (MD022)
        if after_heading and stripped:
            lines.append('')
        after_heading = bool(heading) and not in_code_block
        if after_heading and lines and lines[-1].strip():
            lines.append('')
        # Empty blockquote lines are just ">" (MD027), and one is enough
        if not in_code_block and re.fullmatch(r'[> ]*>', stripped):
            stripped = re.sub(r'> +', '>', stripped)
            if not lines or lines[-1] != stripped:
                lines.append(stripped)
            continue
        # Keep two-space hard line breaks, drop any other trailing whitespace
        if stripped and line.endswith('  '):
            stripped += '  '
        lines.append(stripped)

    # Collapse multiple blank lines
    markdown = re.sub(r'\n{3,}', '\n\n', '\n'.join(lines))

    return markdown.strip()


def create_hugo_file(
        blog: dict, content_dir: Path, dry_run: bool = False
) -> tuple[str, str]:
    """
    Create Hugo markdown file from ERPNext blog.

    Returns:
        Tuple of (filename, status)
    """
    title = blog.get('title', 'Untitled')
    slug = slugify(title)
    filename = f"{slug}.md"
    filepath = content_dir / filename

    # Check if file already exists
    if filepath.exists():
        return filename, 'Exists (skipped)'

    front_matter = blog_to_hugo_frontmatter(blog)
    content = blog_to_hugo_content(blog)

    # Build the file content
    file_content = "---\n"
    file_content += yaml.dump(
        front_matter, default_flow_style=False, allow_unicode=True
    )
    file_content += "---\n\n"
    file_content += content
    file_content += "\n"

    if not dry_run:
        filepath.write_text(file_content)
        return filename, 'Created'
    else:
        return filename, 'Would create'


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
            'Unpublished' if r.get('draft') else 'Published',
            status,
            fidelity_str
        ])

    # Print header
    header = "ERPNEXT BLOG SYNC REPORT"
    if dry_run:
        header += " (DRY RUN)"

    print("\n" + "=" * 80, file=sys.stderr)
    print(f"  {header}", file=sys.stderr)
    print(
        f"  Source: {ERPNEXT.base_url} | "
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        file=sys.stderr)
    print("=" * 80, file=sys.stderr)

    # Print table using tabulate
    headers = ['Title', 'Date', 'Author', 'State', 'Status', 'Fidelity']
    print(tabulate(table_data, headers=headers, tablefmt='simple'),
          file=sys.stderr)

    # Print summary
    print("-" * 80, file=sys.stderr)
    new_count = sum(1 for r in results if r['status'] == 'new')
    unchanged_count = sum(1 for r in results if r['status'] == 'unchanged')
    updated_count = sum(1 for r in results if r['status'] == 'updated')
    error_count = sum(1 for r in results if r['status'] == 'error')
    skipped_count = sum(1 for r in results if r['status'] == 'skipped')
    unpublished_count = sum(1 for r in results if r.get('draft'))

    print(
        f"  Summary: {len(results)} total | {new_count} new | "
        f"{unchanged_count} unchanged | "
        f"{updated_count} updated | {skipped_count} skipped | "
        f"{error_count} errors | {unpublished_count} unpublished",
        file=sys.stderr)
    print("=" * 80, file=sys.stderr)


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


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Sync blog articles from ERPNext with fidelity checking'
    )
    parser.add_argument(
        '--dry-run', '-n', action='store_true',
        help='Show what would happen without writing files'
    )
    parser.add_argument(
        '--force', '-f', action='store_true',
        help='Force overwrite all files, ignoring fidelity check'
    )
    parser.add_argument(
        '--list', '-l', action='store_true',
        help='Only list available blogs, do not sync'
    )
    parser.add_argument(
        '--skip-images', action='store_true',
        help='Skip downloading images'
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Show verbose output'
    )
    args = parser.parse_args()

    script_dir = Path(__file__).parent
    content_dir = script_dir.parent / 'content' / 'blog'
    static_dir = script_dir.parent / 'static'

    if not content_dir.exists():
        print(
            f"Error: Content directory not found: {content_dir}",
            file=sys.stderr
        )
        sys.exit(2)

    if not ERPNEXT.has_credentials:
        print(
            "Warning: API credentials not set; the Blog Post REST API "
            "needs ERPNEXT_API_KEY and ERPNEXT_API_SECRET and may return "
            "HTTP 401/403.",
            file=sys.stderr
        )

    print(f"Fetching blog list from {ERPNEXT.base_url}...", file=sys.stderr)
    blogs = fetch_blogs()

    if not blogs:
        print("No blogs found or error occurred.", file=sys.stderr)
        sys.exit(2)

    unpublished_count = sum(1 for blog in blogs if blog.get('draft'))
    print(
        f"Found {len(blogs) - unpublished_count} published and "
        f"{unpublished_count} unpublished (draft) blogs",
        file=sys.stderr
    )

    if args.list:
        # Just list the blogs
        results = []
        for blog in blogs:
            results.append({
                'title': blog.get('title', 'Untitled'),
                'date': str(blog.get('published_on', ''))[:10],
                'author': blog.get('blogger', 'Unknown'),
                'status': 'available',
                'fidelity': '-',
                'draft': bool(blog.get('draft'))
            })
        print_status_table(results, dry_run=True)
        return

    results = []
    errors_occurred = False

    for i, blog in enumerate(blogs):
        blog_name = blog.get('name')
        if not blog_name:
            continue

        if args.verbose:
            print(
                f"Syncing {i + 1}/{len(blogs)}: "
                f"{blog.get('title', 'Untitled')}",
                file=sys.stderr)

        # Sync the blog
        sync_result = sync_blog(
            blog, content_dir, static_dir,
            dry_run=args.dry_run, force=args.force,
            skip_images=args.skip_images, verbose=args.verbose
        )

        results.append({
            'title': blog.get('title', 'Untitled'),
            'date': str(blog.get('published_on', ''))[:10],
            'author': blog.get('blogger', 'Unknown'),
            'status': sync_result['status'],
            'fidelity': sync_result['fidelity'],
            'file': sync_result.get('file', ''),
            'draft': bool(blog.get('draft'))
        })

    # Output results
    print_status_table(results, dry_run=args.dry_run)

    # Exit code based on errors
    if errors_occurred:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
