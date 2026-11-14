# Architecture

How this repository is meant to be built. Where the code differs today is listed under
"Known deviations". Change this file in the PR that changes the structure.

## What it does

Three things all shrippen projects share: the website `https://shrippen.github.io/`
(the overview of all projects and Kante's stylesheet under `/v1/`, which every landing
page links), the made-up demo world "Studio Weber" every project starts with for
screenshots, and the tools that take these screenshots and put them into the landing
pages. The projects themselves are checkouts next to this repository.

## Building blocks

| Path | Its one task |
|---|---|
| `overview/sites.json` | The list of projects: id, name, folder next to this repository, page address, repository. |
| `overview/projects.json` | What the overview page shows: groups, taglines, live or soon. |
| `overview/tools/build-overview.py` | Builds the overview page `docs/index.html` and collects the project icons. |
| `overview/tools/build-versions.py` | Builds `docs/versions.json`, the latest release of every project, for the apps' update checks. |
| `overview/tools/make-social.py` | Renders the preview image for social networks of every project. |
| `overview/preview/` | The local preview of all landing pages, with what is missing on each. |
| `demo/world/` | The demo world, the only source: one file per topic, the IT notes as Markdown. |
| `demo/world.py` | Merges the world and expands it into `demo/dist/`; also the Python way to read it. |
| `demo/lib/` | The JavaScript and PHP ways to read the world, with the same rules as Python. |
| `demo/dist/` | The built world in the three forms the projects use. Generated, checked in. |
| `demo/tools/sync-demo.py`, `check-demo.py` | Copy the built world into the projects; check that every copy is current. |
| `demo/tools/screenshots.py` | Takes each project's screenshots from its demo. |
| `demo/tools/use-shots.py` | Puts the screenshots into each project's landing page. |
| `demo/kimai/` | A fresh Kimai with the own plug-ins and the demo world, for their screenshots. |
| `docs/` | What GitHub Pages serves. Generated or copied, except the site's own icon: `index.html`, `versions.json`, `social-preview.png`, `assets/icons/`, and `v1/`, an unchanged copy of Kante's build. |
| `build.sh`, `start.sh` | Build `docs/` and run the checks (there is no CI); start the local preview. |
| `tools/` | The structure check, a synced copy from the rules repository. |

## Layers

```
 ../Kante/docs/v1 ──copy──► docs/v1/                 projects next to this repository
                                                        ▲ world      ▲ shots     │ icons,
 overview/sites.json ◄── every tool reads it            │ copies     │ into      │ releases
        │                                               │            │ pages     ▼
        ├─► overview/tools/ ─────────────────────────────────────────────────► docs/
        ├─► overview/preview/
        └─► demo/tools/ ◄── demo/dist/ ◄── demo/world.py + demo/lib/ ◄── demo/world/
```

- Data flows one way: sources (`overview/*.json`, `demo/world/`, Kante) → tools →
  generated files (`docs/`, `demo/dist/`, copies in the projects). Generated files are
  never edited by hand.
- Which projects exist, their folders, names and repositories stand once, in
  `overview/sites.json`. A tool keeps only what it alone needs per project.
- A rule two tools need (the repository of a page, the file name of a screenshot, the
  visitor counter's id, the stylesheet's address) is written once and used by both.
- The demo world has one source, `demo/world/`. Python, JavaScript and PHP read it by the
  same rules; a shared set of examples run through all three holds them equal.
- Projects never read this repository at run time; they get copies. This repository
  reads the projects only through their folders named in `sites.json`.
- Design comes from Kante: `docs/v1/` is never changed here, and no tool copies a colour
  or font by hand; it reads Kante's palette.
- `overview/` and `demo/` know each other only through `overview/sites.json`.

## Where new things go

| Change | Touch |
|---|---|
| A new project | `overview/sites.json`, `overview/projects.json` if it appears on the overview; checklist in `overview/PROJECTS.md` |
| A new group on the overview | `overview/projects.json` only |
| New demo data | The topic file in `demo/world/`, then build and sync |
| A new rule for reading the world | `demo/world.py`, `demo/lib/world.js`, `demo/lib/DemoWorld.php`, and an example for all three |
| A project needs the world in another place or form | `demo/tools/sync-demo.py` |
| Another way to take or name screenshots | `demo/tools/screenshots.py` |
| A design change | Kante, never here |
| A new check of the landing pages | `overview/preview/server.py` |

## Known deviations

- The file name of a screenshot is built in two tools (`AUDIT.md`, finding 1).
- The repository of a page is derived in three tools, one copy wrongly
  (`AUDIT.md`, finding 2).
- The overview page names the groups by hand besides reading them
  (`AUDIT.md`, finding 3).
- The preview-image tool copies colours from Kante's palette by hand and fixes Kante's
  folder (`AUDIT.md`, finding 4).
- The visitor counter's id and the stylesheet's address stand in two tools
  (`AUDIT.md`, finding 5).
- Projects and their folders are listed in five places (`AUDIT.md`, finding 6).
- No test holds the three ways to read the world equal, and they differ already; there
  are no tests at all (`AUDIT.md`, finding 7).
