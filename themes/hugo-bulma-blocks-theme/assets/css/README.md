# assets/css/

All CSS for the theme. **Shared look lives in one file: `theme.css`.** Every
card, button, list, CTA band and prev/next bar on the site is built from the
classes defined there, so a style change made in `theme.css` applies
everywhere.

## Rules

1. **Don't invent a page-prefixed class for a component** (`blog-card`,
   `hosting-cta-buttons`, `team-nav-link`…). Use the theme class and its
   modifiers. If something is missing, add a modifier or part to
   `theme.css`, not a new copy in a page file.
2. Naming follows Bulma: a base class plus `is-*` / `has-*` modifiers, and
   `card-*` for the parts inside a card.
3. Page files (`homepage.css`, `training-booking.css`, inline `<style>`
   blocks) are only for things that exist on one page: hero layouts, the
   contact-page clock and world map, the FAQ accordion, the booking wizard,
   Markdown typography for a page body, etc.
4. Need a hook for JavaScript? Use an `id` or a `data-*` attribute, not a
   styling class.

## `theme.css` reference

### Tokens (`:root`)

Brand colours (`--primary`, `--accent`, `--primary-dark`, `--success`), text
(`--text-dark`, `--text-muted`), neutrals (`--gray-50` … `--gray-900`),
`--shadow-*`, `--radius-*`, `--transition-*`. Use them instead of hex values.

### Buttons (Bulma `.button`)

| Class | Use for |
|---|---|
| `button is-primary` | Main call to action (solid blue) |
| `button is-secondary` | Alternative action beside a primary (blue outline) |
| `button is-accent` | Solid yellow highlight |
| `button is-light` | White button on dark/coloured backgrounds |
| `button-group` | Row of buttons; `is-centered`, `is-right`, `is-vertical` |

Sizes/widths come from Bulma: `is-small`, `is-medium`, `is-large`,
`is-fullwidth`.

### Cards (Bulma `.card`)

| Modifier | Use for |
|---|---|
| `is-tile` | Grid/listing card; fills the column, actions line up at the bottom |
| `is-padded` (+ `is-large`) | Box with padding on the card itself (sidebars, panels) |
| `is-row` | Horizontal card: icon/avatar beside the text |
| `is-flat` | Grey box, no outline (features, "why us") |
| `is-primary` / `is-dark` / `is-accent` | Coloured box with white text |
| `has-border-top` / `has-border-left` | Blue edge; add `has-border-accent` for yellow |
| `is-selected` | Picked state (or put the card right after a checked radio) |

Parts:

| Part | What it is |
|---|---|
| `card-image is-cover` | 16:9 cover image (`is-square` for 1:1, or set `--card-image-ratio`) |
| `card-image is-logo` | Logo shown whole on a white band |
| `card-badge` | Label pinned top-right (`is-success`, `is-info`, `is-danger`) |
| `card-overlay` + `card-overlay-label` | Dark hover layer over an image |
| `card-image-caption` | Dark strip across the bottom of an image |
| `card-header` | Row above the content (icon left, tags right) |
| `card-content` | Body |
| `card-eyebrow` | Small uppercase label above a title |
| `card-title` | Heading; `is-small` for the uppercase sidebar heading |
| `card-subtitle` | Small yellow line under the title |
| `card-description` | Muted body text |
| `card-meta` | Info row (date, author…); `.is-highlight` child for yellow |
| `card-tags` | Row of Bulma `.tag`s |
| `card-quote` | Testimonial text |
| `card-link` | "Read more →" link |
| `card-icon` | Square icon tile (`is-small`, `is-large`, `is-accent`) |
| `card-avatar` | Picture/icon of a person or organisation (`is-light`) |
| `card-list` + `card-list-item` | Stacked rows (links, details); `card-list-content`, `card-list-title`, `card-list-meta` inside; `is-stacked` for title-over-meta; `card-list is-plain` for label/value rows |
| `card-stats` + `card-stat` | Grid of figures (`card-stat-value`, `card-stat-label`) |
| `card-footer` | Bar at the bottom (`card-link` + `card-icon-link`s); `is-centered` |
| `card-icon-link` | Round icon button (share, external link, copy) |

Examples:

```html
<!-- listing tile -->
<article class="card is-tile">
  <div class="card-image is-cover"><a href="…"><img src="…" alt="…"></a></div>
  <div class="card-content">
    <div class="card-meta"><span><i class="fas fa-calendar-alt"></i> 2 Jan 2026</span><span class="is-highlight">Author</span></div>
    <h3 class="card-title"><a href="…">Title</a></h3>
    <p class="card-description">Summary…</p>
    <a class="card-link" href="…">Read more <i class="fas fa-arrow-right"></i></a>
  </div>
</article>

<!-- sidebar box -->
<div class="card is-padded has-border-left">
  <h4 class="card-title is-small"><i class="fas fa-link"></i> Resources</h4>
  <div class="card-list">
    <a class="card-list-item" href="…">
      <span class="card-icon is-small"><i class="fab fa-github"></i></span>
      <span class="card-list-content">Source code</span>
    </a>
  </div>
</div>
```

### Other components

- `checklist`: list with an icon per item (`<li><i class="fas fa-check-circle"></i> <span>…</span></li>`).
- `copy-command`: command line with a copy button.
- `page-nav`: Previous / All / Next bar at the bottom of detail pages.
- `section-cta`: dark CTA band. Don't write it by hand; use
  `{{ partial "section-cta.html" (dict …) }}` (see the partial for parameters).
- Utilities: `is-sticky`, `full-width`, `border-width-2`.

## Load order

Files are concatenated in `partials/header.html`:

```
menu → syntax-highlighter → custom → animate → block → highlight →
bulma-overrides → cookie → homepage → search → engagement → regional →
training-booking → theme → no-motion
```

`theme.css` loads after the page files, so a page tweak to a theme component
needs a more specific selector (e.g. `.blog-section .card-title`).

## Still page-specific (follow-ups)

- Markdown body typography is repeated per page (`.blog-article-content`,
  `.plugin-article-content`, `.course-main`…). It could become one shared
  `.content` style.
- Hero sections (`*-hero`) still use page-prefixed classes.
