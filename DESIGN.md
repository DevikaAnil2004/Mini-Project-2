# CricketIQ design system — "Floodlight"

The interface is a data tool first. Everything below exists to make numbers
readable at a glance and to keep eleven pages looking like one product.

## Scene

A cricket analyst at night, second screen showing a match, wanting dense
figures without glare. Dark is the default; light mode is fully supported for
daytime desk use and is not an afterthought.

## Colour

OKLCH throughout, defined once in `:root` and overridden under
`[data-theme="light"]` in `static/css/style.css`.

| Role | Token | Notes |
| --- | --- | --- |
| Page / sunk / surfaces | `--bg`, `--bg-sunk`, `--surface`, `--surface-2`, `--surface-3` | Cool-tinted graphite ramp (hue 264) |
| Borders | `--line`, `--line-strong` | |
| Text | `--ink`, `--ink-2`, `--muted`, `--faint` | All four hold ≥4.5:1 on `--surface` in both themes |
| Brand | `--accent`, `--accent-fg`, `--on-accent`, `--accent-soft`, `--accent-line` | Floodlight amber |
| Semantic | `--pos`, `--neg`, `--warn`, `--info` (+ `-fg`, `-soft`) | Never the only carrier of meaning — always paired with a label or icon |
| Data viz | `--series-1` … `--series-8` | Hue-spaced; charts read these at runtime |

**Strategy: restrained.** Tinted neutrals plus one accent. Amber is deliberate —
pitch green and analytics blue are the two reflex answers for a cricket
dashboard, and both were rejected.

Two variables per accent matter: `--accent` is a *surface* colour, `--accent-fg`
is the text-safe variant. In light mode they differ (amber on white fails as
text); using the wrong one is the most likely way to break contrast.

## Type

Paired on a contrast axis — sans against mono, not two similar sans faces.

- **Inter Tight** — headings and display, 600/700, tight tracking
- **Inter** — body and UI, 400/500/600
- **JetBrains Mono** — every number, via `.num` / `.mono`, with tabular figures so table columns never jitter

`.num` on a table cell also right-aligns it. `.mono` is the typeface alone —
use it for dates and IDs, which should stay left-aligned.

## Spacing, radius, elevation

4px spacing scale (`--s-1` … `--s-24`). Radius scale `--r-xs` … `--r-full`.
Four elevation steps; dark mode leans on borders plus deep shadow rather than
glow. Never invent a one-off value — if the scale has no step that fits, the
layout is usually the problem.

## Components

One card primitive: `.panel` (with `__head` / `__body` / `__foot`). Cards are
never nested. Other primitives: `.stat-tile`, `.data-table`, `.badge-pill`,
`.btn`, `.field`, `.pager`, `.empty`, `.note`, `.toast`, `.skeleton`,
`.monogram`, `.versus`, `.feature`, `.spotlight`.

Callouts use a full border plus a tinted background — no coloured side stripes.

## Motion

Tokens: `--ease-out` (quart), `--ease-in-out`, and three durations
(`--d-fast` 130ms, `--d-base` 190ms, `--d-slow` 280ms). Micro-interactions stay
under 300ms. Pressable elements scale to 0.975 on `:active`. Reveals enhance
already-visible content — nothing is gated behind a transition that might never
fire. `prefers-reduced-motion: reduce` collapses all of it.

## Accessibility rules the code holds to

- Body text ≥4.5:1, large text ≥3:1, in **both** themes — verified, not assumed
- One amber focus ring on every interactive element; Bootstrap's competing
  `:focus-visible` rules are explicitly overridden, never the ring removed
- Colour is never the sole signal: status, role and result all carry text
- Touch targets reach 44px under `@media (pointer: coarse)` while desktop keeps
  table-dense controls
- Skip link, breadcrumbs, table captions, `aria-sort` on sortable headers,
  `aria-live` on async result panels, labelled form fields with inline errors

## Charts

`static/js/analytics.js` resolves colours from the CSS tokens through a hidden
probe element, so charts re-theme with the page and no hex is duplicated in JS.
Charts degrade honestly: a single season on record renders a ranked bar chart
with an explanatory note instead of an empty line grid.

## Conventions

- Icons come from the SVG sprite in `templates/_icons.html` via `{{ icon('name') }}`
- Shared markup (pagination, empty states, badges, filters) lives in `templates/_components.html`
- Chart.js loads only on pages that draw charts, never from `base.html`
