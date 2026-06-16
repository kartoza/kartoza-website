# Brand alignment audit — 2026-06-16

| | |
| --- | --- |
| Audit target | kartoza.com (this Hugo repo) |
| Aligns against | **Kartoza Brand Pack v1.0.1** |
| Tracking epic | [#165 — Brand alignment](https://github.com/kartoza/kartoza-website/issues/165) |
| Branch | `brand-alignment` |
| Brand pack location (local, gitignored) | `Kartoza_BrandPack_v1.0.1/` |
| Canonical guidelines | `Kartoza_BrandPack_v1.0.1/Kartoza_BrandAssets_v1.0.1/guidelines/Kartoza_Brand_Guidelines.md` |
| Canonical colour tokens | `Kartoza_BrandPack_v1.0.1/Kartoza_BrandAssets_v1.0.1/color/tokens.json` |

> **Purpose.** A single point-in-time snapshot of where this site
> diverges from the brand pack, so every sub-issue under #165 can
> be filed against a concrete finding rather than re-derived from
> scratch.

---

## 0. Reference — canonical Kartoza palette

| Token | Hex | Role |
| --- | --- | --- |
| `kartoza.blue` | `#54A2CC` | Primary accent (links, CTAs, key data, blue trefoil loop) |
| `kartoza.amber` | `#EEB348` | Secondary/highlight accent (callouts, amber trefoil loop) |
| `kartoza.grey` | `#8A8B8B` | Structural mid-grey (grey trefoil loop) |
| `text.default` | `#383939` | Body text, H1/H2, default foreground |
| `text.muted` | `#676869` | Eyebrows, captions, secondary text |
| `rule.line` | `#D1D1D1` | Table rules, dividers, disabled |
| `surface.cloud` | `#F5F5F2` | Page tint, zebra rows, panels |
| `surface.white` | `#FFFFFF` | Base |
| `status.success` | `#3C7D54` / tint `#EAF3EC` | Status only |
| `status.warn` | `#EEB348` / tint `#FCF3E0` | Status only (= brand amber) |
| `status.error` | `#B0473C` / tint `#FBEFEF` | Status only |

Typography (Brand Pack §3.3 + App. B): **Lato** (body + headings,
fallback `Lato, "Helvetica Neue", Arial, sans-serif`), **JetBrains
Mono** (code, fallback `"JetBrains Mono", Consolas, monospace`),
**Lato Italic / semibold in Amber** as the accent/display style.

---

## 1. Executive summary

1. **`config.toml` is the brand-drift epicentre.** Lines 53–98 of
   `[params]` set the site's entire colour and font system, and
   **every value is wrong** — six off-palette blues/ambers and
   `Nunito` set as all three font roles (`heading`, `text`,
   `fancy`). Fixing this one file moves the needle further than
   any other single change.
2. **Closed issue #9 ("Wrong Font Used") was a symptom**, not a
   bug. The root cause has been in `config.toml` the whole time:
   `heading-font = "'Nunito', sans-serif"` at line 96. Until the
   token source is corrected and a lint pre-commit guards it,
   #9-class regressions will keep happening.
3. **Bulma's own defaults are leaking through** — e.g.
   `#00d1b2` (Bulma's stock turquoise `$primary`) in
   `bulma-badge.css`. Phase B1 must override Bulma's Sass
   `$primary` / `$link` / `$family-primary` before the theme
   compiles, not after.
4. **The recently-merged e-commerce layouts** (`cart`,
   `checkout`, `my-orders`, `login`, `reset-password`,
   `payment-complete`, `support-ticket`) carry **hundreds of
   lines of inline `<style>` blocks** with hard-coded
   off-palette hex (`#1a2a3a`, `#3488b8`, `#3b9dd9`,
   `#6b7b8d`, `#e8ecf0`). This is the biggest single cleanup
   surface and should be its own sub-issue.
5. **Logo asset folder needs consolidation.** `static/img/`
   has four "kartoza-logo*" variants of unknown provenance
   (`kartoza-logo.png`, `kartoza-logo-modern.svg`,
   `kartoza-logo-hero.svg`, `kartoza-og-image.svg`) — the brand
   pack ships canonical SVGs (`kartoza-logo-horizontal-color.png`,
   `…-vertical-color.svg`, etc.) that should replace all of them.

---

## 2. The Bulma override surface (load-bearing)

Per decision: **override Bulma's Sass variables before the theme
compiles**, propagating Kartoza tokens to every Bulma component
without per-component patches.

Bulma variables we need to set in a new
`assets/sass/_brand-tokens.scss` (imported before Bulma):

| Bulma variable | Kartoza token | Notes |
| --- | --- | --- |
| `$primary` | `kartoza.blue` `#54A2CC` | Currently inherits Bulma default `#00d1b2` (turquoise) |
| `$link` | `kartoza.blue` `#54A2CC` | Was `#3B9DD9` in config |
| `$info` | `kartoza.blue` `#54A2CC` | Was `#5BB5E8` |
| `$success` | `status.success` `#3C7D54` | Was `#4CAF50` (Material green) |
| `$warning` | `kartoza.amber` `#EEB348` | Was `#E8A331` (drift amber) |
| `$danger` | `status.error` `#B0473C` | Was `#E55B3C` |
| `$black` | `text.default` `#383939` | Was `#1a2a3a` (navy) |
| `$grey-dark` | `text.muted` `#676869` | Was `#3d4f5f` |
| `$grey-light` | `rule.line` `#D1D1D1` | Was `#d4dbe2` |
| `$family-primary` | `Lato, "Helvetica Neue", Arial, sans-serif` | Was Nunito-only |
| `$family-secondary` | `Lato, "Helvetica Neue", Arial, sans-serif` | — |
| `$family-monospace` | `"JetBrains Mono", Consolas, monospace` | Was Fira Code / Roboto Mono mix |
| `$family-sans-serif` | `Lato, "Helvetica Neue", Arial, sans-serif` | — |

---

## 3. Colour audit — top offenders

### 3.1 `config.toml` `[params]` (lines 53–95) — fix first

| Line | Current key | Current value | Replacement | Notes |
| --- | --- | --- | --- | --- |
| 53 | `primary1` | `#53a2cc` | `#54A2CC` | One digit off canonical blue (Brand Pack App. A note) |
| 54 | `primary2` | `#3488b8` | derive from `kartoza.blue` darker shade | Drift blue used heavily downstream |
| 55 | `primary3` | `#b2d5e8` | derive from `kartoza.blue` lighter shade | — |
| 57 | `primary4` | `#9E9E9E` | `kartoza.grey` `#8A8B8B` | Material grey, off-palette |
| 58 | `primary5` | `#C8C8C8` | `rule.line` `#D1D1D1` | — |
| 60 | `primary6` | `#E8A331` | `kartoza.amber` `#EEB348` | **Drift amber** (Brand Pack flags this exact value) |
| 81 | `text-primary1` | `#1a2a3a` | `text.default` `#383939` | Navy, should be Charcoal |
| 82 | `text-primary2` | `#4D6370` | `text.muted` `#676869` | Slate, should be Secondary Grey |
| 89 | `primary` (Bulma) | `#3B9DD9` | `kartoza.blue` `#54A2CC` | Yet another wrong blue |
| 90+ | `danger` `info` `success` `warning` | various | status tokens | See §2 table |

### 3.2 Hex-literal sprawl in layouts (occurrences)

Generated by `rg -No '#[0-9a-fA-F]{3,8}' assets/ layouts/ themes/`.
Top distinct off-palette colours appearing **5+ times**:

| Hex | Occurrences | Where | Replacement |
| --- | --- | --- | --- |
| `#3b9dd9` | 50+ | search.css, regional.css, layouts/my-orders, checkout, document | `kartoza.blue` |
| `#3488b8` | 50+ | login, support-ticket, reset-password layouts | derive from `kartoza.blue` darker |
| `#1a2a3a` | 30+ | cart, checkout, my-orders, support-ticket inline styles | `text.default` |
| `#6b7b8d` | 25+ | login, my-orders, support-ticket | `text.muted` |
| `#e8ecf0` | 15+ | login, search, my-orders | derive cloud-tint or `rule.line` |
| `#edb348` | 8 | theme homepage.css | `kartoza.amber` (drift — note **`edb348` vs canonical `EEB348`**) |
| `#e8a331` | 6 | theme search.css | `kartoza.amber` (Brand Pack's flagged drift amber) |
| `#1b6b9b` | 12 | theme search.css, regional.css | derive from `kartoza.blue` darkest |
| `#00d1b2` | 7 | theme `bulma-badge.css` | Bulma stock `$primary` — must be overridden, not patched |
| `#ee7913` | 6 | theme roadmap.sass | non-palette orange, eliminate |
| `#3a9800` | 6 | theme roadmap.sass | non-palette green — replace with `status.success` |
| `#cc0000` / `#ff0000` | 20+ | theme homepage.css | reds — replace with `status.error` where status; otherwise eliminate |
| `#27ae60` | 6 | theme homepage.css | non-palette green — `status.success` |
| `#00b388` | 6 | course-upcoming-events partial | non-palette teal — likely status, use `status.success` |
| `#1da1f2` | 5 | theme homepage.css | Twitter blue — replace with brand blue or remove if decorative |
| Monokai palette (`#e6db74`, `#a6e22e`, `#66d9ef`, `#ae81ff`, `#75715e`) | 30+ | `highlight.css` | Code syntax theme — **out of scope** (Brand Pack does not dictate syntax colours; just confirm JetBrains Mono is the font) |

### 3.3 Inline `<style>` blocks (line counts of inline-style attrs)

E-commerce layouts merged in the recent 33-commit window carry
the heaviest inline-style debt and should be a single sub-issue:

| File | `style="…"` attr count | Inline `<style>` block? |
| --- | --- | --- |
| `layouts/checkout/single.html` | 24 | yes |
| `layouts/login/single.html` | 18 | yes (large) |
| `layouts/payment-complete/single.html` | 15 | yes |
| `layouts/partials/course-upcoming-events.html` | 15 | yes |
| `layouts/my-orders/single.html` | 14 | yes (large) |
| `layouts/internships/single.html` | 14 | — |
| `layouts/careers/single.html` | 13 | — |
| `layouts/partials/menu.html` | 12 | — |
| `layouts/contact/single.html` | 12 | — |
| `layouts/cart/single.html` | 8 | yes |
| `layouts/support-ticket/single.html` | 6 | yes (large) |
| `layouts/reset-password/single.html` | 6 | yes |
| `layouts/partners/single.html` | 6 | — |

---

## 4. Typography audit

### 4.1 Site-wide config (config.toml lines 95–98)

```toml
heading-font = "'Nunito', sans-serif"   # → 'Lato', "Helvetica Neue", Arial, sans-serif
text-font    = "'Nunito', sans-serif"   # → same
fancy-font   = "'Nunito', sans-serif"   # → Lato Italic (accent/display style, Brand Pack FR-022)
```

### 4.2 Theme-bundled `bulma.sass` overrides

`themes/hugo-bulma-blocks-theme/assets/sass/bulma.sass` declares
`@font-face` for **five** non-Kartoza families:

| Line | Family | Action |
| --- | --- | --- |
| 38 | `Montserrat` | Remove / replace with Lato |
| 42–62 | `Trueno` (×5 weights) | Remove — Lato covers the weight range |
| 67 | `Twemoji Country Flags` | Keep — emoji flags, not brand |
| 74 | `Work Sans` | Remove — replaced by Lato |
| 80 | `'Sevillana', cursive` | Remove — decorative cursive, off-brand |

### 4.3 Monospace inconsistency

Different files have picked different monospace stacks:

| Surface | Current stack | Replacement |
| --- | --- | --- |
| `theme/homepage.css` (3 sites) | `'Fira Code', 'Monaco', monospace`, `'Roboto Mono', monospace`, `'SF Mono', 'Monaco', 'Inconsolata', monospace` | `"JetBrains Mono", Consolas, monospace` |
| `syntax-highlighter.css` | `Consolas, "Liberation Mono", Courier, monospace` | same |
| `layouts/cart/single.html` etc. (inline) | `monospace` (system default) | same |

No `@font-face` declaration for Lato or JetBrains Mono exists
anywhere. **Both fonts are simply not loaded**, so any
`font-family: Lato …` declaration today falls back silently to
the system default. (This explains the Nunito everywhere
default — it must be loaded by the theme or browser fallback we
haven't yet traced; needs a quick Phase A2 confirmation.)

### 4.4 Fonts to bundle (Phase A2)

Copy from `Kartoza_BrandPack_v1.0.1/Kartoza_BrandAssets_v1.0.1/fonts/`:

- `Lato-Regular.ttf`
- `Lato-Italic.ttf`
- `Lato-Bold.ttf`
- `Lato-BoldItalic.ttf`
- `Lato-Black.ttf`
- `JetBrainsMono.ttf`

→ Place in `static/webfonts/` (Font Awesome already lives there;
naming is consistent). Add `@font-face` block in
`assets/sass/_brand-tokens.scss` with `font-display: swap` to
avoid invisible text on cold load.

---

## 5. Logo audit

### 5.1 Inventory — `static/img/` Kartoza-branded files

| Current file | Provenance | Action |
| --- | --- | --- |
| `kartoza-logo.png` | unknown variant | replace with `kartoza-logo-horizontal-color.png` from brand pack |
| `kartoza-logo-hero.svg` | hero-page bespoke | retire; use canonical SVG |
| `kartoza-logo-modern.svg` | "modern" variant of unknown spec | retire |
| `kartoza-brand-pattern.svg` | pattern asset | replace with `kartoza-motif.png` / `slant_divider.png` from brand pack |
| `kartoza-og-image.svg` | OpenGraph social card | regenerate using brand pack vertical lockup + motif |
| (none) — favicon | — | add `kartoza-favicon-64.png` + `kartoza-appicon-512.png` from `logos/` |

### 5.2 Lockup variants the brand pack ships (FR-001..006)

To be copied into `static/img/brand/`:

```
kartoza-logo-horizontal-color.{png,svg}
kartoza-logo-horizontal-mono.png
kartoza-logo-horizontal-reversed.png
kartoza-logo-vertical-color.{png,svg}
kartoza-logo-vertical-mono.png
kartoza-logo-vertical-reversed.png
kartoza-symbol-color.svg
kartoza-symbol-mono.png
kartoza-symbol-reversed.png
kartoza-appicon-512.png
kartoza-favicon-64.png
```

→ Then introduce a Hugo partial `layouts/partials/brand-logo.html`
taking a `variant` parameter; every header/footer/partner-card
usage must route through it. Closes the "many one-off logo
references" problem at compile time.

### 5.3 Clear-space + minimum size (FR-004 / FR-005)

Audit deferred to Phase B2 when the partial is in place — clear
space is enforced by CSS padding around the partial, not by
individual call sites.

---

## 6. Imagery audit (initial)

Off-brand patterns to look for during Phase D (motif & imagery):

- **Stock photography used as primary visuals** — Brand Pack
  FR-033 explicitly prohibits. Likely candidates: any `unsplash`,
  `pexels` filenames in `static/img/`. Quick check pending.
- **Drop-shadowed clip art / gradients / bevels** — search for
  `box-shadow:` + `background: linear-gradient` in Sass. Initial
  scan: theme uses gradients heavily; needs flat-design pass.
- **Isometric illustrations** (retired style) — visual review
  required, no programmatic signal.
- **Twitter blue `#1da1f2`** in homepage.css suggests social
  iconography uses platform colours rather than monochrome
  brand-grey icons — Brand Pack §3.5 prefers single-style icons.

---

## 7. Page-by-page rollup

| Surface | Primary debts | Sub-issue owner phase |
| --- | --- | --- |
| Homepage (`/`) | hex literals in `homepage.css` (15+ off-palette), gradients, social colours | F1 |
| Services / Solutions | depends on tokens landing | F2 (+ E2 icons) |
| Projects / Apps | partner & client lockups need B3 co-brand partial | F3 |
| Partners | already has #147 baseline (BGEO) — extend pattern | F7 + B3 |
| Training | `course-upcoming-events.html` has `#00b388` and `#edb348` drift | F4 |
| Blog | typography + callouts + code blocks | F5 + C3 + C5 |
| YouTube | rebuilt by #164 — confirm header/footer chrome only | F6 (light touch) |
| **E-commerce (new)** — cart, checkout, my-orders, login, reset-password, payment-complete, support-ticket | **heaviest inline-style debt; ~hundreds of off-palette literals** | **new sub-issue: F9 — e-commerce inline-style purge** |
| 404 / empty states | not yet audited | F8 |
| Footer (`partials/footer.html`) | inline `font-family: monospace; color: rgba(255,255,255,0.4)` | bundle into A3 |
| Menu (`partials/menu.html`) | 12 inline-style attrs | bundle into B1 (header chrome) |

---

## 8. Recommended sub-issues to file from this audit

Refines and extends epic #165's Phase-A..G checklist with what
we now know is actually in the code. Each is intended to be one
PR off `brand-alignment`:

1. **A1 — Token foundation.** `assets/sass/_brand-tokens.scss`
   derived from `tokens.json`, imported before Bulma. Overrides
   Bulma's `$primary`, `$link`, `$info`, `$success`, `$warning`,
   `$danger`, `$black`, `$grey-dark`, `$grey-light`, all four
   font families. Replaces every value in `config.toml` lines
   53–98. ~150 lines, no visible diff yet — purely token rails.
2. **A2 — Self-host Lato + JetBrains Mono.** Six font files into
   `static/webfonts/`; `@font-face` block in `_brand-tokens.scss`;
   remove `Montserrat`/`Trueno`/`Work Sans`/`Sevillana`
   `@font-face` from `themes/hugo-bulma-blocks-theme/assets/sass/bulma.sass`.
   Verify with cold-cache load.
3. **A3 — Hex-literal lint.** `scripts/check-no-raw-hex.sh`
   (grep for `#[0-9a-fA-F]{3,8}` in `assets/`, `layouts/`,
   `content/`; allow-list canonical palette + monokai syntax).
   Wire into pre-commit + GH Actions. **This is the durable fix
   for closed #9 recurring.**
4. **A4 — Purge config.toml drift values.** Delete the
   `primary1…6`, `text-primary1/2`, `link`, `links`,
   `complementary1…8`, `light1…3`, `dark1/2` parameters now
   that the token file is canonical. Audit theme templates for
   any remaining `.Site.Params.primary*` references; replace
   with token classes/utilities.
5. **B1 — Logo partial + canonical SVGs.**
   `layouts/partials/brand-logo.html` (variants:
   `horizontal-color | vertical-color | symbol | …-reversed |
   …-mono | favicon | appicon`). Replace all current header /
   footer / OG-image logo references. Drop the four legacy
   `kartoza-logo*` files from `static/img/`.
6. **C1+C2 — Type scale + eyebrow.** Sass mixins for `Title`,
   `Subtitle`, `H1`–`H4`, `Body`, `Caption`, `Code`, `Eyebrow`
   matching Brand Pack App. B. Eyebrow is the "KARTOZA · X"
   letter-spaced uppercase pattern.
7. **F9 — E-commerce inline-style purge.** Move all hex
   literals out of the seven e-commerce layouts (`cart`,
   `checkout`, `my-orders`, `login`, `reset-password`,
   `payment-complete`, `support-ticket`); replace with token
   classes. This is the single largest cleanup PR; do it after
   A1+A2 are merged so the replacements actually exist.
8. **G1 — WCAG 2.2 AA contrast check** of the new token
   combinations using Pa11y or `axe-core` in the existing
   Playwright e2e suite.
9. **G2 — Visual regression baseline.** Playwright screenshot
   suite before any further visual change, so every subsequent
   PR has a diff to review.
10. **G3 — `/docs/brand.md`** quick-reference for contributors:
    "to add a new page on-brand, use these tokens, this partial,
    this type-scale class."

---

## 9. Out of scope (explicit)

- Office templates and Marp/MkDocs themes — those are the Brand
  Pack's own delivery surfaces, not the website's.
- GSH / QGIS Cloud product UIs (Brand Pack §1.2 exclusion).
- Code syntax highlighting palette — Brand Pack does not dictate.
  Keep current Monokai; only ensure JetBrains Mono is the font.
- ERPNext-synced content (training events, jobs feed) — we can
  restyle containers but not the source data.

---

_Made with ❤️ by Kartoza · audit: `tim@kartoza.com` · 2026-06-16_
