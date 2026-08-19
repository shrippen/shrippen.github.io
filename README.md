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
- **Feature grid**: `--bg1` cards, `--bg2` border, `1.2rem` gap, `auto-fit minmax(240px, 1fr)`.
- **Screenshot**: `--radius` corners, `1px --bg2` border, deep `box-shadow`.
- **Badges**: shields.io with `labelColor=1c1c20` and value color `e8dcc4` (version), `83a598` (tech tag), `a89984` (license).
- **OG image**: dark card on `--bg-hard`, project icon centered, name below in `--fg0`, tagline in `--fg2`.
- **Max content width**: `--max-w` (`860px`). Centered with `margin: 0 auto`.
- **No light mode** for landing pages (matches the dark-first palette). Plasma widgets use whatever the user's Plasma theme provides.
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

- **Size**: 1280×640 px
- **Background**: `--bg-hard` (`#1d2021`)
- **Icon**: Project mark (cream), centered, 128 px
- **Title**: `--fg0`, 48 px, system sans bold, below icon
- **Tagline**: `--fg2`, 20 px, below title
- **Bottom strip**: subtle `--bg2` line at ~580 px, then `--fg3` one-liner "github.com/shrippen/<project>"

---

## File structure of this repo

```
DesignDefault/
├── README.md              ← this document
├── tokens/
│   ├── variables.css      ← CSS custom properties
│   ├── palette.json       ← machine-readable palette
│   └── palette.qml        ← QML QtObject for Plasma widgets
├── templates/
│   └── landing.html       ← starter landing page
└── examples/
    └── badge-strip.svg    ← sample badge layout
```

---

## Using in another project

**Landing page**: copy `tokens/variables.css` into your `docs/` or inline the `:root` block. Follow the layout template.

**Plasma widget**: reference the palette philosophy (accent cream, deterministic project hashes, priority bands). Do not import CSS — use `Kirigami.Theme.*` for all dynamic colors and only hardcode the shared accent (`#E8DCC4`) for brand elements.

**README badges**: use the badge format above.

**Icons**: follow the icon language (24×24 viewbox, cream mark, themed variant).

---

*Palette derived from [Gruvbox](https://github.com/morhetz/gruvbox) by morhetz (MIT). Adapted with a warm-cream brand accent for the shrippen project family.*
