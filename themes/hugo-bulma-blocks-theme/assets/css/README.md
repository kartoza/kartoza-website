# assets/css/

This folder contains all CSS for the theme. We are actively migrating toward a
**component-based architecture** — styles are being moved out of large,
page-scoped files and into a small set of reusable classes that any layout can
use.

## Migration goal

Much of the markup was generated page by page, so every page invented its own
class names for the same thing: `blog-card`, `portfolio-card`, `training-card`,
`app-card`… or `about-cta-buttons`, `hosting-cta-buttons`,
`plugin-cta-buttons`… all with near-identical rules copied into
`homepage.css`. Fixing a style meant fixing it in dozens of places, and the
copies drifted apart.

The fix is one shared theme. **Before writing a new class, check whether
`theme.css` already has it.** Only add page-specific CSS for things that are
genuinely unique to that page, and build them on top of the theme classes.

## Key files to know

### `theme.css`

The site's theme: design tokens plus the reusable components. Naming follows
Bulma — a base class plus `is-*` / `has-*` modifiers.

**Tokens** (`:root`): brand colours (`--primary`, `--accent`, `--primary-dark`),
text (`--text-dark`, `--text-muted`), neutrals (`--gray-50` … `--gray-900`),
`--shadow-*`, `--radius-*`, `--transition-*`. Use these instead of hard-coded
hex values.

**Buttons** (extend Bulma's `.button`):

| Class | Use for |
|---|---|
| `button is-primary` | The main call to action (solid blue) |
| `button is-secondary` | The alternative action beside a primary (blue outline) |
| `button is-accent` | Solid yellow highlight |
| `button is-light` | White button on dark or coloured backgrounds |
| `is-outlined` | Outline version of `is-primary` / `is-accent` |

Sizes and widths come from Bulma: `is-small`, `is-medium`, `is-large`,
`is-fullwidth`.

**Button group**: `button-group`, with `is-centered`, `is-right`, `is-vertical`.

```html
<div class="button-group is-centered">
  <a class="button is-primary is-medium" href="…">Get started</a>
  <a class="button is-secondary is-medium" href="…">Learn more</a>
</div>
```

**Cards** (extend Bulma's `.card`):

| Class | Use for |
|---|---|
| `card` | Base surface: white, rounded, outlined |
| `card is-tile` | Grid/listing card: full column height, links aligned at the bottom |
| `card is-padded` (`is-large`) | Sidebar/info box with padding on the card itself |
| `card is-flat` | Grey box with no outline (features, "why us") |
| `card is-primary` / `is-dark` / `is-accent` | Coloured CTA box with white text |
| `has-border-top` / `has-border-left` | Blue edge; add `has-border-accent` for yellow |

Card parts: `card-image is-cover` (fixed-ratio image, 16:9 by default; set
`--card-image-ratio` to change it), `card-content`, `card-title`
(`is-small` for the uppercase sidebar heading), `card-subtitle`,
`card-description`, `card-link`.

```html
<article class="card is-tile">
  <div class="card-image is-cover"><img src="…" alt="…"></div>
  <div class="card-content">
    <h3 class="card-title">Title</h3>
    <p class="card-description">Summary…</p>
    <a class="card-link" href="…">Read more <i class="fas fa-arrow-right"></i></a>
  </div>
</article>

<aside class="card is-padded has-border-left">
  <h4 class="card-title is-small">Tags</h4>
  …
</aside>
```

### `components.css`

Styles for discrete, named UI components that appear in more than one layout
and are too specific for the theme (e.g. `main-card` on the homepage).

See `components/README.md` for the conventions on when to split a component into
its own file under `components/`.

## Load order

Files are concatenated in `partials/header.html` in this order:

```
menu → syntax-highlighter → custom → animate → block → highlight →
bulma-overrides → cookie → homepage → search → engagement → regional →
training-booking → components → theme → no-motion
```

`theme.css` loads after the page-level files so its rules take precedence over
Bulma and page-level overrides. Page-specific tweaks to a theme component
therefore need a more specific selector (e.g. `.blog-list .card-title`), not
an edit to `theme.css`.

## What still needs migrating

Replace the page-prefixed classes in the layouts with the theme classes, then
delete the old rules from `homepage.css`. Typical mappings:

| Old (examples) | New |
|---|---|
| `*-cta-buttons` (`about-`, `hosting-`, `plugin-`, `team-`, `solution-`…) | `button-group is-centered` |
| `sidebar-cta-buttons` | `button-group is-vertical` |
| `button is-outlined is-primary` | `button is-secondary` |
| `blog-card`, `portfolio-card`, `training-card`, `gallery-card`, `app-card`, `solution-card`, `plugin-card` | `card is-tile` |
| `*-card-image` | `card-image is-cover` |
| `*-card-content` | `card-content` |
| `*-card-title` / `*-card-description` / `*-card-link` | `card-title` / `card-description` / `card-link` |
| `sidebar-card`, `filter-sidebar-card`, `partner-sidebar-card`, `gallery-sidebar-card` | `card is-padded` |
| `sidebar-card-title` | `card-title is-small` |
| `*-why-card`, `benefit-card`, `hosting-feature-card`, `why-us-card` | `card is-flat is-padded has-text-centered` |
| `*-cta-card` | `card is-padded is-primary` (or `is-dark`) |
| `upstream-card`, `related-card` | `card is-padded has-border-left` (`has-border-accent` for yellow) |

Do this one layout at a time, and check that page in the browser before
removing the old CSS: some old classes carry small extras (an overlay, a
badge position) that should stay as page-specific rules.
