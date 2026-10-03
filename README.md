# shrippen.github.io

This repository is the user site of [shrippen](https://github.com/shrippen) and has two parts, one folder each, and serves the Kante build:

| Folder | Part | Documentation |
|---|---|---|
| [`overview/`](overview) | **Overview page** of all projects at <https://shrippen.github.io/>, generated from `overview/projects.json`, and the local preview of all landing pages | [overview/README.md](overview/README.md) |
| [`demo/`](demo) | **Demo data and screenshots**: the shared demo world „Studio Weber“, the Kimai demo instance and the tools that sync the world into the projects and take their landing-page screenshots | [demo/README.md](demo/README.md) |

**Rule for all projects:** every GUI is generated from Kante, not inspired by it, and a missing element is added to Kante first. Kimai plugins are the one exception, they use Knust, Kante's spinoff for Kimai. See [`AGENT-RULE.md`](https://github.com/shrippen/Kante/blob/main/AGENT-RULE.md).

**Kante lives in its own repository, [shrippen/Kante](https://github.com/shrippen/Kante)** (checkout `../Kante`), together with Knust and the Kimai plugin kit. This repo only copies its build: `build.sh` takes `../Kante/docs/v1/` unchanged into `docs/v1/`, so every landing page keeps linking `https://shrippen.github.io/v1/shrippen.css`.

Kante was called *shrippen Design Default* before; file names and URLs keep the old `shrippen` prefix so nothing that links them breaks.

GitHub Pages serves the `docs/` folder (Settings → Pages → `main`, `/docs`). Run `./build.sh` after every change to Kante (after `./build.sh` in `../Kante`) or to `overview/projects.json`, and commit the result in `docs/`.

## File structure

```
shrippen.github.io/
├── README.md              ← this document
├── build.sh               ← builds docs/: copies Kante's docs/v1, builds the overview page, checks its tokens
├── start.sh               ← local preview of all landing pages (overview/preview/)
├── docs/                  ← GitHub Pages source, served at https://shrippen.github.io/ (generated, do not edit by hand)
│   ├── index.html         ← overview page
│   ├── icon.svg, icon-mono.svg, social-preview.png
│   ├── assets/icons/      ← project icons copied by overview/tools/build-overview.py
│   └── v1/                ← Kante's build, copied from ../Kante/docs/v1 (shrippen.css, shrippen.js, fonts, knust-palette.css)
├── overview/
│   ├── projects.json      ← projects on the overview page
│   ├── sites.json         ← all project landing pages (id, name, folder, URL)
│   ├── PROJECTS.md        ← landing-page status, checklist for new projects
│   ├── preview/           ← local preview server and UI, todos.json
│   └── tools/             ← build-overview.py, make-social.py
├── demo/
│   ├── world/             ← the demo world (source, one file per topic), world.py builds dist/
│   ├── lib/, dist/        ← loaders and the built copies for the projects
│   ├── kimai/             ← shared Kimai demo instance for all Kimai plugins
│   └── tools/             ← sync-demo.py, check-demo.py, screenshots.py, use-shots.py (.venv for playwright)
```

## License

All rights reserved. This repository is public for reference only and is not intended for public use. See [LICENSE](LICENSE).
