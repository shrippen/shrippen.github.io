# Projects using the shrippen design system

Tracking list and to-do list: which landing pages follow (or still need to be migrated to) the shared design. The central stylesheet is
`https://shrippen.github.io/DesignDefault/v1/shrippen.css` (see [README](README.md)).

**Status legend**

- `central` — links the central stylesheet
- `palette` — uses the shared palette and badge colors, but not yet the central stylesheet
- `todo` — not yet checked or migrated

| Project | Page | Status | Known deviations / to do |
|---|---|---|---|
| Plasmai | https://shrippen.github.io/Plasmai/ | palette | Backend table needs the `.table` component |
| Kurrent | https://shrippen.github.io/Kurrent/ | palette | Plasma badge uses `#3daee9`, should be `#83a598` |
| PaperTTY | https://shrippen.github.io/PaperTTY/ | palette | Emojis as feature icons, replace with inline SVG (`.feat-icon`); displays table needs `.table` |
| FrameWidge | https://shrippen.github.io/FrameWidge/ | palette | Release badge uses `#b8bb26`, should be `#e8dcc4`; AI-disclaimer fits `.callout-warn` |
| PaperNinja | https://shrippen.github.io/PaperNinja/ | palette | Uses a nav bar (`.nav`), numbered setup (`.steps`), emoji feature icons, architecture diagram (`.codeblock`) |
| dolphin-davinci-audio-tools | https://shrippen.github.io/dolphin-davinci-audio-tools/ | todo | Design not verified; has nav and a conversions table |
| kimai-holiday-bundle | https://shrippen.github.io/kimai-holiday-bundle/ | palette | Permissions and REST endpoint tables need `.table` |

## To do: projects to bring into the system

Repositories that should get the design system later. No landing page is tracked yet, so their status is `todo`.
When one gets a page, move it into the table above.

| Project | Repository | Status | Note |
|---|---|---|---|
| companion-mpris | https://github.com/shrippen/companion-mpris | todo | Add later; page URL not yet known |
| darktable-auto-crop | https://github.com/shrippen/darktable-auto-crop | todo | Add later; page URL not yet known |
| kimai-abrechnung-bundle | https://github.com/shrippen/kimai-abrechnung-bundle | todo | Add later; page URL not yet known. Sibling of kimai-holiday-bundle, should share its layout |

"palette" is inferred from the badge colors visible on each page. Whether a page actually loads the shared tokens
or Rajdhani has not been checked in its source. Update the status when a page is migrated.

## Adding a project

1. Start from [`templates/landing.html`](templates/landing.html) and link the central stylesheet.
2. Add a row to the table above.
