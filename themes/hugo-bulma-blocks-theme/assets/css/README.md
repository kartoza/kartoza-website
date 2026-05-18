# assets/css/

This folder contains all CSS for the theme. We are actively migrating toward a
**component-based architecture** — styles are being moved out of large,
page-scoped files and into focused, reusable files that can be shared across any
layout.

## Migration goal

The old approach scattered styles across page-specific files (e.g. `homepage.css`,
`training-booking.css`). The new approach isolates reusable styles into dedicated
files so that any layout can use them without pulling in unrelated rules.

## Key files to know

### `button.css`

The single source of truth for all button styles across the site.

Previously, button variants (size, colour, border, hover state) were defined
separately inside each page-level CSS file. This caused drift — the same button
class looked different depending on which page you were on.

**All new or updated button styles go here. Do not add button rules elsewhere.**

### `theme.css`

Site-wide design tokens and global overrides that apply across all pages —
typography scale, colour variables, spacing defaults, and any rules that need to
sit above Bulma but below component-specific styles.

**Use this file for global rules. Do not use it for component or button styles.**

### `components.css`

Styles for discrete, named UI components that appear in more than one layout —
cards, badges, section banners, grids, etc.

See `components/README.md` for the conventions on when to split a component into
its own file under `components/`.

**All new reusable component styles go here (or in `components/`).**

## Load order

Files are concatenated in `partials/header.html` in this order:

```
menu → syntax-highlighter → custom → animate → block → highlight →
bulma-overrides → cookie → homepage → search → engagement → regional →
training-booking → components → theme → button
```

`button.css` and `theme.css` load last so their rules take precedence over
Bulma and page-level overrides.

## What still needs migrating

- Button rules inside `homepage.css`, `training-booking.css`, and other
  page-scoped files should move to `button.css`.
- Repeated component patterns (sidebar cards, CTA banners, grids) should move
  to `components.css` or a dedicated file under `components/`.
