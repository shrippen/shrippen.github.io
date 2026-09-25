# Projects using the shrippen design system

Tracking list: which landing pages follow the shared design. The central stylesheet is
`https://shrippen.github.io/v1/shrippen.css` (see [README](README.md)).

**Status legend**

- `central` — links the central stylesheet
- `palette` — uses the shared palette and badge colors, but not yet the central stylesheet
- `todo` — not yet checked or migrated

| Project | Page | Status | Notes |
|---|---|---|---|
| Plasmai | https://shrippen.github.io/Plasmai/ | central | Extended page in `Plasmai/docs/index.html` (showcases, flow, FAQ, roadmap); on branch `landing-page-redesign` |
| Kurrent | https://shrippen.github.io/Kurrent/ | central | Extended page in `Kurrent/docs/index.html` (views, Quick Add, flow, FAQ, roadmap; v0.4.0); on branch `landing-page-redesign` |
| PaperTTY | https://shrippen.github.io/PaperTTY/ | central | Extended page in `PaperTTY/docs/index.html` (three inline SVG graphics, modes, how it works, install, options, FAQ); no photos yet |
| FrameWidge | https://shrippen.github.io/FrameWidge/ | central | Extended page in `FrameWidge/docs/index.html` (tab showcases, tray, flow, install, config, FAQ); notices are `.callout` |
| PaperNinja | https://shrippen.github.io/PaperNinja/ | central | Extended page in `PaperNinja/docs/index.html` (scoring, screens, flow, config, security, FAQ; two screenshots) |
| dolphin-davinci-audio-tools | https://shrippen.github.io/dolphin-davinci-audio-tools/ | central | Migrated locally; conversions table uses `.table`; has a "Why this exists" section (Resolve on Linux has no AAC) |
| kimai-holiday-bundle | https://shrippen.github.io/kimai-holiday-bundle/ | central | Extended page in `Kimai Holiday Plugin/docs/index.html` (absences, working times, calendar, holidays, install, FAQ); permissions table and API `.codeblock` |
| companion-mpris | https://shrippen.github.io/companion-mpris/ | central | New page in `companion/mpris/docs/`; one screenshot |
| kader (formerly darktable-auto-crop) | https://shrippen.github.io/kader/ | central | Extended page in `kader/docs/` (status banner "Work in progress", standalone web UI first, targets table, darktable plugin as one option, three install routes incl. Windows/Linux packages, placeholder graphics instead of screenshots, FAQ) |
| kimai-abrechnung-bundle | https://shrippen.github.io/kimai-abrechnung-bundle/ | central | Extended page in `Kimai Abrechnung/AbrechnungBundle/docs/` (workflow, billing levels, FAQ) |
| kimai-drehzettel-bundle | https://shrippen.github.io/kimai-drehzettel-bundle/ | central | New page in `Kimai Drehzettel/docs/index.html` (status banner "Early development", features with ready/planned tags, timesheet showcase, flow, TV FFS rules `.table`, phases, FAQ); mockup SVG instead of a screenshot; page is on `main`, not on `landing-page-redesign` |
| kimai-anfahrten | https://shrippen.github.io/kimai-anfahrten/ | central | New page in `Kimai Anfahrten/docs/index.html` (callout "calculation aid, not tax advice", features, Dawarich, logbook, tax, team showcases with the README screenshots, flow, install, permissions `.table`, FAQ); `page_live` false, the roadmap postpones Pages |

"central" means the page links the central stylesheet and script. **Not live yet**: every project has the new page on the branch `landing-page-redesign` (pushed to the Gitea `origin`, based on `main`, or `master` for kimai-holiday-bundle), so nothing goes live before it is merged. The stylesheet only resolves once GitHub Pages is enabled for the repo `shrippen.github.io` (Settings → Pages → `main`, `/docs`) and the built `docs/v1/` is pushed; do that first, then merge the branches.

## Website material (`docs/`)

Rule: screenshots, the logo (`icon.svg`) with its monochrome twin (`icon-mono.svg`) and everything else the page uses live in the project's own `docs/` folder.

| Project | Logo | Screenshots in `docs/` |
|---|---|---|
| Kurrent | Check and wave (A) | yes (4, plus 3 detail crops) |
| Plasmai | Half ring clock (B) | yes (3, plus 1 detail crop) |
| PaperNinja | Mask badge (E) | yes (2: suggestion, linked; document thumbnails and titles pixelated) |
| PaperTTY | Ink drop (F) | no. Upstream photos exist in `pics/` but are not this fork's own |
| FrameWidge | Chip with fan (B) | yes (4, one per tab; cropped from `dist/1-4.png`, taskbar removed) |
| kimai-holiday-bundle | Umbrella (C) | yes (3: absence page, working times, absence calendar; names and hours pixelated) |
| dolphin-davinci-audio-tools | Fin (B) | yes (2: context menu with the KDE Connect device name pixelated, progress dialog with file names pixelated) |
| companion-mpris | Key cap (C) | yes (1: button page; track info pixelated) |
| kader | Film cell (F) | no. Four placeholder SVGs (`placeholder-*.svg`) stand in for before/after, detection debug image, results by label and the darktable panel |
| kimai-abrechnung-bundle | Receipt (A) | yes (1: billing overview; customers, projects, tasks and employees pixelated) |
| kimai-drehzettel-bundle | Film frame with check (E) | no. `timesheet-preview.svg` (made-up data, A4 landscape mockup of the PDF) stands in for a screenshot |
| kimai-anfahrten | Route to a pin (new, not from Logo Studio) | yes (5 of 6 used: trips, detected trips, logbook, tax report, team; test data) |

Every project also has `docs/social-preview.png` (generated by `tools/make-social.py`, referenced by `og:image`). Logos were picked from the Logo Studio artifact. Each has `icon.svg` and `icon-mono.svg` in `docs/`. Old landing-page logos are removed (`PaperNinja/docs/logo.png` and `social.png`; its README and DESIGN.md point to the new files). App icons are separate. Plasmai (`contents/images/icon.*`, `icons/`) and PaperNinja (`app/static/`) show the new logo. Kurrent's `icons/` show the new two-colour logo (the old `logo.png` in the repo root was removed). FrameWidge's tray icon is the monochrome new logo and its app icon the accent version.

## Adding a project

1. Start from [`templates/landing.html`](templates/landing.html) and link the central stylesheet.
2. Add a row to the table above.
3. Add the project to `preview/sites.json` (id, name, folder, page URL) and to `projects.json` (group, tagline, `page_live`), then run `./build.sh` so it appears on the overview page. Set `page_live` to `true` once its GitHub Pages site is enabled and merged.
