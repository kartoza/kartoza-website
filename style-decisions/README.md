# Style decisions needed

On `main`, these components should share one theme style but are styled
differently from page to page. For each case the PR (`theme/reusable-components`)
currently uses one option, marked **PR now**. Please pick which style is correct.

Each image shows `main` on the left (black labels) and the PR on the right (red labels).

| # | Image | Options seen on `main` | PR now |
|---|---|---|---|
| 01 | [01-card-padding.png](01-card-padding.png) | Card padding: **2rem** (homepage product cards, office cards, hosting pathways) · **1.5rem 2rem 2rem** (blog/training listing cards) · **1.5rem** (blog sidebar, partner blocks, footer offices) · **1.75rem** (team sidebar) | **2rem** for every card (`--card-padding`, 1.5rem on mobile) |
| 02 | [02-card-badge-position.png](02-card-badge-position.png) | Card badge: **top-left** over the image (homepage carousel) · **top-right** over the image (training courses) · **on the top edge, right** (hosting pathways) | **Top-left** over the image; on cards without an image, in the header row on the right |
| 03 | [03-card-list-marker.png](03-card-list-marker.png) | List items in a card: **check icon** (homepage featured card) · **blue dot** (homepage product cards) | **Check icon** everywhere (`.checklist`) |
| 04 | [04-card-title-size.png](04-card-title-size.png) | Card title: **1rem** (homepage partners) · **1.25rem** (blog, training, carousel) · **1.5rem** (homepage product cards) | **1.25rem** everywhere (`.card-title`); featured cards use `.card-title.is-large` (2rem) |
| 05 | [05-icon-accent-colour.png](05-icon-accent-colour.png) | Icon tiles: **yellow** (partner Key Features, support-ticket lock, homepage "Why Work With Kartoza") · **blue** (about, most others) | **Blue** (`.card-icon`); yellow is `.card-icon.is-accent` |
| 06 | [06-meta-highlight-colour.png](06-meta-highlight-colour.png) | Highlighted text in plugin card meta: client name **blue** · in-house "By: Kartoza" **yellow** | **Yellow** (`.card-meta .is-highlight`) |
| 10 | [10-cta-box-style.png](10-cta-box-style.png) | CTA boxes: **blue box** (partner sidebar "Get Started Today", plugin CTA band) · **dark band** (most pages) · **white card** | Section CTA = dark band; sidebar CTA = `card is-primary` (blue) |

Once a style is chosen, the change is one value in `themes/hugo-bulma-blocks-theme/assets/css/theme.css`.
