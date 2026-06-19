# Rewrite

A modern, restrained Hugo theme for **kartoza.com**.
Aligned with the **Kartoza Brand Pack v1.0.1**.

No CSS framework. No build step beyond Hugo Pipes. Flat colour.
Type-driven hierarchy. WCAG 2.2 AA. Dark mode. View transitions.

**Signature hero:** solid Kartoza charcoal panel with the map motif
clipped to a slanted polygon on the right edge and an amber slant
rule between the two halves.

---

## Adoption model

This theme runs **in a theme chain** alongside
`hugo-bulma-blocks-theme` while page types are migrated one at a
time. In your site's `config.toml`:

```toml
theme = ["rewrite", "hugo-bulma-blocks-theme"]
```

Hugo looks in `rewrite` first; anything not yet authored falls
through to the legacy theme. Migrate per-section by adding
`layouts/<section>/single.html` (or `list.html`) to this theme,
or by removing the project-level override at
`/layouts/<section>/…`.

---

## File layout

```
rewrite/
├── theme.toml
├── README.md
├── archetypes/default.md
├── assets/
│   ├── css/
│   │   ├── 00-tokens.css     ← design tokens
│   │   ├── 01-reset.css      ← modern reset
│   │   ├── 02-base.css       ← element defaults
│   │   ├── 03-layout.css     ← layout primitives
│   │   ├── 04-components.css ← chrome + hero + cards + buttons
│   │   └── 05-utilities.css  ← single-property helpers
│   └── js/app.js             ← vanilla, ~50 lines
└── layouts/
    ├── _default/{baseof,list,single}.html
    ├── index.html            ← full homepage
    ├── partials/
    │   ├── head.html
    │   ├── seo.html
    │   ├── nav.html
    │   ├── rw-footer.html    ← namespaced to win Hugo lookup
    │   ├── breadcrumb.html
    │   ├── skip-link.html
    │   ├── page-meta.html
    │   └── pagination.html
    └── shortcodes/           ← 1:1 vocabulary with upstream
        ├── block.html         block-section.html
        ├── button.html        button-bar.html
        ├── columns-start.html columns-end.html
        ├── column-start.html  column-end.html
        ├── feature-card.html  hero-banner.html
        ├── info-bar.html      list-content.html
```

---

## Design system

All styling consumes CSS custom properties declared in
`assets/css/00-tokens.css`.  Change a token, every component
picks up the new value.

**Palette** — Brand Pack App. A: `#54A2CC` blue, `#EEB348` amber,
`#383939` charcoal, `#676869` muted, `#D1D1D1` rule, `#F5F5F2`
cloud, `#FFFFFF` white, plus semantic status colours.

**Type scale** — modular ratio 1.25, base 16 px.  Fluid display
sizes via `clamp()` for headlines.

**Spacing scale** — 4-px base: `--space-1` (4 px) through
`--space-11` (160 px).

**Layout primitives** (Every Layout-inspired):
`.container`, `.section`, `.stack`, `.cluster`, `.grid`,
`.sidebar`, `.switcher`, `.cover`, `.frame`, `.center`,
`.reel`, `.spread`, `.visually-hidden`.

**Hero** — two variants:

- `.hero` — clean canvas, dark text, for interior pages where
  content carries the visual weight.
- `.hero hero--inverse` — the **signature**: solid charcoal
  panel, map motif clipped to a slanted polygon on the right
  edge, amber slant rule between the halves, content (text +
  CTAs) on the left ~45 %.

**Dark mode** — automatic via `prefers-color-scheme`; opt out
via `data-color-scheme="light"` on `<html>`, opt in via
`data-color-scheme="dark"`.

**Reduced motion** — `prefers-reduced-motion` zeros transition
durations.

**Print** — separate print rules in `02-base.css`.

---

## Shortcode vocabulary

Same parameter API as the upstream `hugo-bulma-blocks-theme`:

| Shortcode       | Parameters                                   |
| --------------- | -------------------------------------------- |
| `button`        | `text`, `link`, `icon`, `class`, `fullwidth` |
| `button-bar`    | positional `"icon:text:link"` triples (self-closing) |
| `columns-start` | `id`                                         |
| `columns-end`   | —                                            |
| `column-start`  | `size` (accepted for compat)                 |
| `column-end`    | —                                            |
| `block`         | `title`, `subtitle`, `class`, `link`, `link-text`, `image`; inner |
| `block-section` | `backgroundColor`, `textColor`, `subtitle`, `title`, `class`; inner |
| `feature-card`  | `icon`, `title`, `class`; inner              |
| `hero-banner`   | positional title; inner subtitle             |
| `info-bar`      | positional `"Label:Value"` pairs (self-closing) |
| `list-content`  | inner bulleted markdown                      |

Anything not in this list still resolves through the legacy
theme via the chain.

---

## Kartoza credit

Made with 💗 by **[Kartoza](https://kartoza.com)** ·
[Donate!](https://github.com/sponsors/kartoza) ·
[GitHub](https://github.com/kartoza/kartoza-website)
