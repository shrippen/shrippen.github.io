# shrippen.github.io

This repository is the user site of [shrippen](https://github.com/shrippen) and has two jobs:

1. **Overview page** of all projects at <https://shrippen.github.io/>. It is generated from [`projects.json`](projects.json) by `tools/build-overview.py`.
2. **shrippen Design Default**, the shared design system that every project landing page links to (documented below). The built stylesheet is served at `https://shrippen.github.io/v1/shrippen.css`.

GitHub Pages serves the `docs/` folder (Settings → Pages → `main`, `/docs`). Run `./build.sh` after every change to `css/`, `js/`, `tokens/` or `projects.json`, and commit the result in `docs/`.

---

# shrippen Design Default

Shared design language for [shrippen](https://github.com/shrippen) projects.
Each project keeps its own local Plasma/Kirigami/GTK theme integration — this document defines the **shared accent palette, typographic rules, icon style, and landing-page layout** that make the family feel cohesive.

Gruvbox-inspired, warm, dark-first.

---

## Quick reference

| Token | Hex | Role |
|---|---|---|
| `bg-hard` | `#1d2021` | Deepest background (hero, code blocks) |
| `bg0` | `#282828` | Page / widget background |
| `bg1` | `#3c3836` | Cards, elevated surfaces |
| `bg2` | `#504945` | Borders, dividers, subtle outlines |
| `fg0` | `#fbf1c7` | Primary heading text (sparingly) |
| `fg1` | `#ebdbb2` | Body text |
| `fg2` | `#d5c4a1` | Secondary / muted text |
| `fg3` | `#a89984` | Placeholder, disabled, footer |
| `accent` | `#e8dcc4` | Brand warm-cream (icon fills, hero emphasis) |
| `blue` | `#83a598` | Primary action, links, interactive |
| `aqua` | `#8ec07c` | Success, confirm, online |
| `green` | `#b8bb26` | Positive diff, badges |
| `yellow` | `#fabd2f` | Warnings, attention |
| `orange` | `#fe8019` | Active / highlight |
| `red` | `#fb4934` | Error, destructive, high priority |
| `purple` | `#d3869b` | Tags, categories, decorative |

Use the **neutral** variant (e.g. `#458588` instead of `#83a598`) when the bright version is too loud on dark surfaces. Use the **faded** variant for disabled / pressed states.

See [`tokens/`](tokens/) for CSS custom-properties, QML, and SVG exports.

---

## Palette philosophy

The palette is a **warm-shifted Gruvbox Dark** subset.

- **Background** is Gruvbox `dark0` (`#282828`), not pure black. `bg-hard` (`#1d2021`) is reserved for maximum-depth areas (hero gradients, code blocks).
- **Foreground** is Gruvbox `light1` (`#ebdbb2`) for body and `light0` (`#fbf1c7`) for headings. Never pure white.
- **Brand accent** is `#e8dcc4` — the cream tone already used in the Kurrent icon mark and badges. This is the family's signature: monochrome icon fills and version badges use it.
- **Primary action** color is Gruvbox `bright_blue` (`#83a598`), not KDE's Breeze blue — but in Plasma widgets the native `Kirigami.Theme.highlightColor` takes over; the shared blue only applies to web pages and standalone assets.
- The remaining Gruvbox brights slot into semantic roles (aqua = success, orange = highlight, red = error, etc.) so every project draws from the same well without inventing one-off hues.

### Light theme ("Leinen")

Opt-in for apps (not landing pages) via `<html data-theme="light">`, defined in [`tokens/variables.css`](tokens/variables.css). Token names describe **roles, not lightness**: `--bg-void` is always the page ground, `--bg-panel` the cards, `--bg2` the borders, `--fg1` the body text. Switching the theme only swaps values.

| Token | Dark | Light | Role |
|---|---|---|---|
| `bg-void` | `#141312` | `#f0e9d6` | Page ground |
| `bg-panel` | `#2a2826` | `#f7f2e4` | Cards, panels |
| `bg1` | `#3c3836` | `#fbf8ee` | Elevated / fields |
| `bg-hard` | `#1d2021` | `#e6dec6` | Sunk areas, tracks |
| `bg2` | `#504945` | `#d3c8ac` | Borders |
| `fg1` | `#ebdbb2` | `#3c3836` | Body text |
| `fg2` | `#d5c4a1` | `#665c54` | Secondary text |
| `blue` | `#83a598` | `#076678` | Action, links |
| `aqua` | `#8ec07c` | `#427b58` | Success, bars |
| `yellow` | `#fabd2f` | `#8a5a00` | Score, warnings |
| `orange` | `#fe8019` | `#af3a03` | Active / highlight |
| `red` | `#fb4934` | `#9d0006` | Error |

The ground sits between Gruvbox `light0` (`#fbf1c7`, too yellow) and `#f5f1e8` (too bright); cards are one step lighter than the ground but never white. **Sand** (`#ebe3cf` ground, `#f4eedd` cards) is the darker alternative. Semantic colors are the darkened counterparts, so all text pairs reach WCAG AA. The role tokens `--field`, `--score` (yellow) and `--hl` (orange) follow the theme. Icon: on light grounds use a dark square (`#3c3836`) with the yellow marks.

### App components (`.tile`, `.stage`, `.band`, `.field`, `.pill`, `.dialog`, …)

Landing pages do not need them; apps do (used by the Darktable Auto Crop companion UI). They follow the theme roles (`--field`, `--score`, `--hl`, `--scrim`), so they work in the dark default and in the light theme. Image stages stay dark in both themes on purpose (judging colour on a beige ground is misleading). Group colours: green `--aqua`, yellow `--yellow`, red `--red`; status is never colour alone. Reference cards live in `ds-bundle/components/App/`. Behaviour (dragging, handles, locking) is the app's job.

### Local theme override rule

> Plasmoids **never hardcode** these hex values for interactive UI. Body text, highlight, selection, buttons, and scrollbars come from `Kirigami.Theme.*`. The shared palette is for **accent elements that survive a theme switch** — icon color fills, priority bands, project/label hashes, and the brand mark in the About/config header.

Landing pages, README badges, social-preview images, and documentation use the full shared palette directly.

---

## Typography

| Context | Stack | Weight | Size guidance |
|---|---|---|---|
| Landing hero heading | `'Rajdhani', var(--font-sans)` | 700 | `clamp(2.2rem, 5vw, 3.4rem)` |
| Section headings (h2, h3) | `'Rajdhani', var(--font-sans)` | 600 | `1.3rem` / `1rem` |
| Feature card headings | `'Rajdhani', var(--font-sans)` | 600 | `1rem` |
| Body | System sans (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif`) | 400 | `1rem` / `16px`, line-height `1.6` |
| Code / commands | `'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace` | 400 | `0.85rem` |
| Plasma widget | `Kirigami.Theme.defaultFont` | — | Let Plasma decide |

[Rajdhani](https://fonts.google.com/specimen/Rajdhani) is the shared heading typeface — squared, condensed, slightly futuristic. It loads via Google Fonts (`wght@600;700`) on landing pages. Body text stays on the system sans stack for readability and zero FOUT. Plasma widgets ignore Rajdhani entirely and use `Kirigami.Theme.defaultFont`.

---

## Icon language

All shrippen icons share these constraints:

| Rule | Detail |
|---|---|
| Viewbox | `0 0 24 24` (matches Breeze and most Plasma icon themes) |
| Fill color | `#E8DCC4` (accent cream) for the monochrome "mark" variant |
| Stroke | None for mark variants; if a bicolor icon is needed, stroke `currentColor` with `stroke-width="2"` and `stroke-linecap="round"` / `stroke-linejoin="round"` |
| Shape language | Rounded corners, soft geometry. No sharp 90° intersections unless depicting a clear UI metaphor (checkbox, grid). |
| Themed variant | A second SVG that uses `class="ColorScheme-Text"` + `fill="currentColor"` so Plasma icon themes recolor it |

The "mark" (cream on transparent) is for landing pages, social previews, and About sections. The themed variant is the panel/tray icon.

### Naming convention

```
icons/<project>-mark.svg     # fixed cream fill, for web & branding
icons/<project>.svg           # themed, for Plasma icon themes
```

---

## Landing page template

Every project landing page follows the same vertical rhythm:

```
┌──────────────────────────────┐
│         Icon (88px)          │
│        Project Name          │
│     One-line tagline         │
│   [version] [tech] [license] │
│                              │
│  ┌────────────────────────┐  │
│  │  Install one-liner     │  │
│  │  [copy] [download]     │  │
│  └────────────────────────┘  │
│   [Primary CTA] [GitHub]     │
├──────────────────────────────┤
│       Screenshot / demo      │
├──────────────────────────────┤
│   Feature grid (2–3 cols)    │
├──────────────────────────────┤
│   Prerequisites / How it     │
│   works (prose list)         │
├──────────────────────────────┤
│         Footer               │
│  license · author · issues   │
└──────────────────────────────┘
```

### Rule: website material lives in `docs/`

Every project keeps **all screenshots and other material used by its landing page in the `docs/` folder of its own repository**, next to `docs/index.html`. That includes a version of the logo:

```
<project>/docs/
├── index.html
├── icon.svg        ← logo, cream with a yellow accent; used in the nav and as favicon
├── icon-mono.svg   ← the same logo in one colour only (cream)
├── screenshot.jpg  ← screenshots, referenced with relative paths
└── social.png      ← optional social preview (og:image)
```

Every logo comes in two versions: `icon.svg` (cream with the yellow accent) and `icon-mono.svg` (a fully monochrome version, one colour). Recolour the mono file for light backgrounds or print. The pages are served from `docs/` on GitHub Pages, so pages never reference files outside it. If a project has no screenshot yet, the hero shows only the install box.

### CSS variables (shared)

Every landing page imports these variables (or copies them):

```css
:root {
  /* Backgrounds */
  --bg-hard:  #1d2021;
  --bg0:      #282828;
  --bg1:      #3c3836;
  --bg2:      #504945;

  /* Foregrounds */
  --fg0:      #fbf1c7;
  --fg1:      #ebdbb2;
  --fg2:      #d5c4a1;
  --fg3:      #a89984;

  /* Accent */
  --accent:   #e8dcc4;

  /* Semantic */
  --blue:     #83a598;
  --aqua:     #8ec07c;
  --green:    #b8bb26;
  --yellow:   #fabd2f;
  --orange:   #fe8019;
  --red:      #fb4934;
  --purple:   #d3869b;

  /* Layout */
  --radius:   12px;
  --max-w:    860px;

  /* Type */
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
               Ubuntu, Cantarell, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, monospace;
}
```

### Rules

- **Background**: `--bg0` for the page, `--bg1` for cards/elevated, `--bg-hard` for hero gradient or code blocks.
- **Text**: `--fg1` body, `--fg0` hero heading only, `--fg2` secondary, `--fg3` footer/placeholders.
- **Links & primary buttons**: `--blue`. Hover darkens 10%.
- **Install card**: `--bg1` surface, `--bg2` border, `--bg-hard` inner code box, command text in `--blue`.
- **Copy button**: `--bg2` bg, on success flash `--aqua` border + text for 1.5 s.
- **Icons in feature cards**: inline SVG (`.feat-icon`, 24×24, stroke `currentColor`) — no emojis.
- **Feature grid**: `--bg1` cards, `--bg2` border, `1.2rem` gap, `auto-fit minmax(240px, 1fr)`.
- **Screenshot**: `--radius` corners, `1px --bg2` border, deep `box-shadow`.
- **Badges**: shields.io with `labelColor=1c1c20` and value color `e8dcc4` (version), `83a598` (tech tag), `a89984` (license).
- **OG image**: dark card on `--bg-hard`, project icon centered, name below in `--fg0`, tagline in `--fg2`.
- **Max content width**: `--max-w` (`860px`). Centered with `margin: 0 auto`.
- **No light mode** for landing pages (matches the dark-first palette). Apps may opt in to the Light theme below; Plasma widgets use whatever the user's Plasma theme provides.
- **Mobile**: Install command box font shrinks to `0.75rem`, hero padding reduces. Feature grid collapses to 1 col.

---

## Plasma widget rules

Inside a KDE Plasma widget, the **shared palette is secondary**. Plasma themes control surfaces, text, and interactive colors.

Use the shared design for:

| Element | Source |
|---|---|
| Project/label accent hashes | Deterministic HSL from key (same algorithm), `saturation: 0.62`, `lightness: 0.46` |
| Priority bands | Red / yellow-amber / blue at fixed HSL (see Kurrent `colors.js`) |
| Icon mark fill in About/header | `#E8DCC4` |
| Badge backgrounds (version label) | `#E8DCC4` on `#1c1c20` |
| `PluginMissing` / onboarding | Layout follows landing page install-card pattern (copy button, monospace command, link to GitHub) |

Do **not** use the shared palette for:

- Button backgrounds, text colors, selection, scrollbars, list backgrounds → `Kirigami.Theme.*`
- Anything the user expects to change with their Plasma color scheme

---

## Badge format

For shields.io badges in READMEs and landing pages:

```
https://img.shields.io/badge/<label>-<value>-<valueColor>?labelColor=1c1c20
```

| Badge | Value color | Example |
|---|---|---|
| Version | `e8dcc4` | `version-0.2.0-e8dcc4?labelColor=1c1c20` |
| Tech/platform | `83a598` | `Plasma-6-83a598?labelColor=1c1c20` |
| License | `a89984` | `license-GPL--3.0-a89984?labelColor=1c1c20` |

---

## Social preview / OG image

`docs/social-preview.png` in every project, referenced by `og:image` (plus `og:image:width/height` and `twitter:card=summary_large_image`). Generated, not hand-made: `python3 tools/make-social.py [id ...]` renders it from the project's `docs/icon.svg` (needs chromium). Run it again after a logo change. Also upload it under Settings → Social preview of the GitHub repo.

- **Size**: 1280×640 px
- **Background**: `--bg-hard` (`#1d2021`)
- **Logo**: colour version (`icon.svg`), centered, 144 px
- **Title**: project name in Rajdhani 700, uppercase, spaced, `--fg0`, up to 76 px (shrinks for long names)
- **Tagline**: `--fg2`, 26 px, system sans
- **Bottom strip**: `--bg2` line at 580 px, then `--fg3` mono line `github.com/shrippen/<repo>`

---

## File structure of this repo

```
shrippen.github.io/
├── README.md              ← this document
├── projects.json          ← projects shown on the overview page (name, group, tagline, page live or soon)
├── start.sh               ← local preview of all landing pages (preview/)
├── build.sh               ← builds docs/v1/ and the overview page docs/index.html
├── css/
│   ├── base.css           ← reset, body, links
│   └── components.css     ← all landing-page components
├── js/shrippen.js         ← language switch, nav brand reveal, copy button
├── docs/                  ← GitHub Pages source, served at https://shrippen.github.io/
│   ├── index.html         ← overview page (generated, do not edit by hand)
│   ├── icon.svg, icon-mono.svg, social-preview.png
│   ├── assets/icons/      ← project icons copied by tools/build-overview.py
│   └── v1/                ← built artifacts (shrippen.css, shrippen.js)
├── tokens/
│   ├── variables.css      ← CSS custom properties
│   ├── palette.json       ← machine-readable palette
│   └── palette.qml        ← QML QtObject for Plasma widgets
├── templates/
│   └── landing.html       ← starter landing page
├── tools/                 ← make-social.py (social previews), build-overview.py
└── examples/
    └── badge-strip.svg    ← sample badge layout
```

---

## Local preview of all landing pages

```bash
./start.sh            # http://127.0.0.1:8080/, next free port if busy (PORT=9000 ./start.sh, NO_OPEN=1 ./start.sh)
```

Sidebar on the left lists every project page with what is missing or could be improved; the selected page opens in the viewport on the right (Desktop / Tablet / Phone width). Sites are listed in `preview/sites.json`, hand-written to-dos live in `preview/todos.json`; checks like missing files, placeholders, screenshot and og:image are derived from each project's `docs/`. The preview serves the local stylesheet instead of the GitHub Pages one and strips the Umami script. Only the Python standard library, bound to 127.0.0.1.

---

## Using in another project

**Landing page**: link the central stylesheet — no copy, changes propagate to every page:

```html
<link href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://shrippen.github.io/v1/shrippen.css">
<script src="https://shrippen.github.io/v1/shrippen.js"></script>  <!-- in <head>, not deferred -->
```

`shrippen.js` handles the language switch, the nav brand reveal and the copy button. Pages are **English by default** with a DE switch: every visible text exists twice (`lang="en"` / `lang="de"`), the choice is stored in `localStorage`. The project name in the nav fades in once the hero has left the viewport. The hero carries a **watermark**: `<img class="hero-wm" src="icon-mono.svg" alt="" aria-hidden="true">` as the first child of `header.hero` (huge, 7 % opacity, bleeding off the right edge and, on a short hero, below it; scrolls with the page, never fixed). The page ends with a **signature footer** (`footer.foot`): the colour logo (`icon.svg`), project name and tagline, two link columns (Project / Source) and, under a short yellow line, license · author · version. A project that is not ready yet puts a full-width **banner** (`.banner` with `.banner-inner`, `.banner-title`, `.banner-text`; `.banner-danger` for red) as the very first element of `<body>`, above the nav. Hazard stripes on its top and bottom edge come from the component itself. A vibe-coded, experimental or unofficial project shows one notice as `<div class="section"><div class="callout callout-warn">` that is always the **first element in `<main>`**, before the facts strip and the features. A project built on or forked from another one adds “based on” or “fork of” to that line, and the name is always a link to the upstream repository (in both languages, for example `<span lang="en">based on <a href="…">name</a></span><span lang="de">basiert auf <a href="…">name</a></span>`). On tablet and phone (≤900px) the hero is one column: `<br class="split">` line breaks in the name are dropped, so the name is written out in full, and its size follows the width (`--title-size-narrow`, about `154/longest-word-length` vw). The Rajdhani font link now also loads JetBrains Mono (see the template).

**Every landing page carries the Umami tracker** in its `<head>`, the same tag with the same website ID on all pages (`<script defer src="https://um.arianw.de/script.js" data-website-id="056d39ee-6a9d-4b14-9902-5a1ac399df08"></script>`); it is already in the template, so do not remove or change it. The local preview strips the script, so visits there are not counted. Start from `templates/landing.html`. Components: nav (with `.lang` switch), facts strip (`.facts`), showcase rows (`.showcase`, screenshot beside text), architecture flow (`.flow`), input-syntax tokens (`.tokens`), FAQ (`.faq`), `<kbd>`, hero (big name left, yellow install box and screenshot right, both the same width), buttons, feature boxes with a colour bar on top (`data-tier="red|yellow|blue"`), prose section, steps, table, codeblock, callout, footer with a short yellow line. All boxes have only the top-right corner cut (`--chamfer`). Page ground is `--bg-void`, cards are `--bg-panel`. Breaking changes ship as `/v2/`; `/v1/` stays stable.

**Plasma widget**: reference the palette philosophy (accent cream, deterministic project hashes, priority bands). Do not import CSS — use `Kirigami.Theme.*` for all dynamic colors and only hardcode the shared accent (`#E8DCC4`) for brand elements.

**README badges**: use the badge format above.

**Icons**: follow the icon language (24×24 viewbox, cream mark, themed variant).

---

*Palette derived from [Gruvbox](https://github.com/morhetz/gruvbox) by morhetz (MIT). Adapted with a warm-cream brand accent for the shrippen project family.*

## License

All rights reserved. This design system is public for reference only and is not intended for public use. See [LICENSE](LICENSE).
