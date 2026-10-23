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


def comparable_text(markdown: str) -> str:
    """Normalize markdown so cleanup-only changes don't count as changes.

    Applies the same cleanup as new content, and ignores code fences, which
    older content had as indented code blocks.
    """
    markdown = clean_markdown(fix_list_markers(markdown))
    markdown = re.sub(r'^\s*```.*$', '', markdown, flags=re.MULTILINE)
    return normalize_for_comparison(markdown)


def fetch_blog_list() -> list[dict]:
    """Fetch list of all published blog posts using the public list API with pagination."""
    blogs = []
    limit_start = 0
    page_size = 20

    while True:
        url = f"{ERPNEXT.base_url}/api/method/frappe.www.list.get"
        params = {
            'doctype': 'Blog Post',
            'limit_start': limit_start,
            'pathname': '/blog'
        }

        try:
            response = ERPNEXT.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            print(
                f"Error fetching blog list "
                f"(page {limit_start // page_size + 1}): {e}",
                file=sys.stderr)
            break
        except json.JSONDecodeError as e:
            print(f"Error parsing blog list response: {e}", file=sys.stderr)
            break

        message = data.get('message', {})
        raw_result = message.get('raw_result', '[]')

        # Parse the raw_result JSON string
        try:
            page_blogs = json.loads(
                raw_result) if isinstance(raw_result, str) else raw_result
        except json.JSONDecodeError:
            page_blogs = []

        if not page_blogs:
            break

        # Transform to our format
        for blog in page_blogs:
            route = blog.get('route', '')
            blogs.append({
                'name': f"/{route}" if route and not route.startswith(
                    '/') else route,
                'title': blog.get('title', 'Untitled'),
                'blog_category': blog.get('blog_category', 'uncategorised'),
                'published_on': blog.get('published_on', ''),
                'blogger': blog.get('blogger', 'Kartoza'),
                'content': blog.get('content', ''),
                'cover_image': blog.get('cover_image', ''),
                'modified': blog.get('published_on', ''),
                # Use published date as modified
            })

        # Check if there are more pages
        show_more = message.get('show_more', False)
        next_start = message.get('next_start', 0)

        if not show_more or next_start <= limit_start:
            break

        limit_start = next_start

    return blogs


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
    """Find the first image URL in a blog post's content."""
    if post.get('content_type') == 'Markdown':
        match = re.search(
            r'!\[[^\]]*\]\(<?([^)>\s]+)', post.get('content_md') or ''
        )
        return match.group(1) if match else ''

    content = post.get('content') or post.get('content_html') or ''
    img = BeautifulSoup(content, 'html.parser').find('img', src=True)
    return img['src'] if img else ''


def fetch_unpublished_blogs() -> list[dict]:
    """Fetch unpublished blog posts using the authenticated REST API.

    The public list API only returns published posts, and unpublished posts
    have no public page to scrape, so the content comes from the API too.
    These are synced as Hugo drafts.
    """
    fields = [
        'name', 'title', 'route', 'blogger', 'blog_category', 'published_on',
        'creation', 'blog_intro', 'meta_image', 'content_type', 'content',
        'content_md', 'content_html',
    ]
    try:
        response = ERPNEXT.get(
            f"{ERPNEXT.base_url}/api/resource/Blog Post",
            params={
                'filters': json.dumps([['published', '=', 0]]),
                'fields': json.dumps(fields),
                'limit_page_length': 0,
            }
        )
        response.raise_for_status()
        posts = response.json().get('data', [])
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error fetching unpublished blogs: {e}", file=sys.stderr)
        return []

    blogger_names = {}
    blogs = []
    for post in posts:
        category = post.get('blog_category') or 'uncategorised'
        route = post.get('route') or f"blog/{category}/{post['name']}"
        # Same category source as published posts: the URL path
        parts = route.strip('/').split('/')
        if len(parts) >= 3:
            category = parts[1]

        blogger = post.get('blogger') or 'Kartoza'
        if blogger not in blogger_names:
            blogger_names[blogger] = fetch_blogger_name(blogger)

        published_on = post.get('published_on') or post.get('creation') or ''
        blogs.append({
            'name': f"/{route.strip('/')}",
            'title': post.get('title') or 'Untitled',
            'blog_intro': post.get('blog_intro') or '',
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
            'draft': True,
        })

    return blogs


def fetch_blog_detail(name: str) -> dict | None:
    """
    Fetch full blog post details.

    Since fetch_blog_list now returns full details, this function just returns
    the blog data if it was passed directly, or fetches from the web page as fallback.
    """
    # If name is already a dict with full data, return it
    if isinstance(name, dict):
        return name

    # Fallback: scrape the public blog page
    url = f"{ERPNEXT.base_url}{name}"

    try:
        response = ERPNEXT.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching blog '{name}': {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract metadata from meta tags
    def get_meta(attr_name, attr_value):
        tag = soup.find('meta', attrs={attr_name: attr_value})
        return tag.get('content', '') if tag else ''

    # Get title from og:title (has proper capitalization) or meta name
    title = get_meta(
        'property', 'og:title'
    ) or get_meta('name', 'title') or get_meta(
        'name', 'name'
    )
    if not title:
        h1 = soup.find('h1', class_='blog-title')
        title = h1.get_text(strip=True) if h1 else 'Untitled'
    # Clean up title prefix
    title = re.sub(r'^Kartoza\s*-\s*', '', title)

    # Get description/intro
    description = get_meta(
        'name', 'description'
    ) or get_meta('property', 'og:description')
    if not description:
        intro = soup.find('p', class_='blog-intro')
        description = intro.get_text(strip=True) if intro else ''

    # Get author - prefer full name from avatar/author link over meta tag username
    author = None
    # Try to get full name from avatar span
    avatar_span = soup.find('span', class_='avatar', attrs={'title': True})
    if avatar_span:
        author = avatar_span.get('title')
    # Or from author link
    if not author:
        author_link = soup.find(
            'a', href=lambda h: h and '/blog?blogger=' in h
        )
        if author_link:
            author = author_link.get_text(strip=True)
    # Fallback to meta tag
    if not author:
        author = get_meta(
            'name', 'author'
        ) or get_meta('property', 'og:author') or 'Kartoza'

    # Get published date
    published_on = get_meta(
        'name', 'datePublished'
    ) or get_meta('property', 'og:published_on')
    if not published_on:
        time_tag = soup.find('time', attrs={'datetime': True})
        published_on = time_tag['datetime'] if time_tag else ''

    # Get featured image
    image = get_meta('name', 'image') or get_meta('property', 'og:image') or ''

    # Get content from article body
    content = ''
    article_body = soup.find('div', attrs={'itemprop': 'articleBody'})
    if article_body:
        content = str(article_body)

    # Extract category from URL path
    parts = name.split('/')
    category = parts[2] if len(parts) >= 3 else 'uncategorised'

    return {
        'name': name,
        'title': title,
        'blog_intro': description,
        'blogger': author,
        'published_on': published_on,
        'modified': published_on,  # Use published date as modified
        'blog_category': category,
        'content': content,
        'featured_image': image,
    }


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
    # Get thumbnail from cover_image (API) or featured_image (scraping) or use placeholder
    thumbnail = blog.get(
        'cover_image', ''
    ) or blog.get('featured_image', '') or PLACEHOLDER_IMAGE
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

    # Take code blocks out first, so html2text and the list fixes can't
    # mangle them
    html, code_blocks = extract_code_blocks(fix_quill_lists(content))

    # Convert HTML to markdown
    markdown = fix_list_markers(h.handle(html))

    return clean_markdown(restore_code_blocks(markdown, code_blocks))


CODE_BLOCK_PLACEHOLDER = 'KARTOZACODEBLOCK'


def extract_code_blocks(html: str) -> tuple[str, list[str]]:
    """Replace <pre> blocks with placeholders and render them as fenced code.

    Quill stores each code line as a <div class="ql-code-block"> and indents
    with non-breaking spaces, which html2text turns into code with a blank
    line after every line.
    """
    soup = BeautifulSoup(html, 'html.parser')
    code_blocks = []

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
    for line in markdown.split('\n'):
        stripped = line.rstrip()
        if stripped.lstrip().startswith(('```', '~~~')):
            in_code_block = not in_code_block
        # Drop empty headings like "###", but not "#" comments in code
        if not in_code_block and re.fullmatch(r'#{1,6}', stripped):
            continue
        # Drop spaces inside inline code: "a ` code `." -> "a `code`." (MD038)
        if not in_code_block and '``' not in stripped:
            stripped = re.sub(
                r'`( *)([^`\n]*?[^ `\n])( *)`',
                lambda match: trim_code_span(match, stripped), stripped
            )
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

    print(f"Fetching blog list from {ERPNEXT.base_url}...", file=sys.stderr)
    blogs = fetch_blog_list()

    if not blogs:
        print("No blogs found or error occurred.", file=sys.stderr)
        sys.exit(2)

    unpublished_blogs = fetch_unpublished_blogs()
    print(
        f"Found {len(blogs)} published and {len(unpublished_blogs)} "
        f"unpublished (draft) blogs",
        file=sys.stderr
    )
    blogs += unpublished_blogs

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

        # Fetch full blog content by scraping the web page (has proper HTML formatting)
        if args.verbose:
            print(
                f"Fetching {i + 1}/{len(blogs)}: "
                f"{blog.get('title', 'Untitled')}",
                file=sys.stderr)
        # Unpublished blogs have no public page, but already have content
        if blog.get('draft'):
            blog_detail = blog
        else:
            blog_detail = fetch_blog_detail(blog_name)
        if not blog_detail:
            results.append({
                'title': blog.get('title', 'Untitled'),
                'date': str(blog.get('published_on', ''))[:10],
                'author': blog.get('blogger', 'Unknown'),
                'status': 'error',
                'fidelity': '-',
                'file': '',
                'draft': bool(blog.get('draft'))
            })
            errors_occurred = True
            continue

        # Sync the blog
        sync_result = sync_blog(
            blog_detail, content_dir, static_dir,
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
