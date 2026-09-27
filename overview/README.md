# Overview page

The overview of all projects at <https://shrippen.github.io/>, plus the local preview of every landing page. Paths in this document are relative to the repo root.

| File | What it is |
|---|---|
| `overview/projects.json` | projects shown on the overview page (group, tagline, page live or soon) |
| `overview/sites.json` | every project with a landing page: id, name, folder next to this repo, page URL. Also read by `demo/tools/screenshots.py` and `overview/tools/make-social.py` |
| `overview/PROJECTS.md` | status of the landing pages and the checklist for adding a project |
| `overview/tools/build-overview.py` | builds `docs/index.html` and copies each project's `docs/icon.svg` to `docs/assets/icons/` (`./build.sh` runs it) |
| `overview/tools/make-social.py` | renders `docs/social-preview.png` for every project (needs chromium; spec in [Kante](../kante/README.md#social-preview--og-image)) |
| `overview/preview/` | the local preview (`server.py`, `index.html`, hand-written to-dos in `todos.json`) |

`docs/index.html` is generated: edit `projects.json` and run `./build.sh`.

## Local preview of all landing pages

```bash
./start.sh            # http://127.0.0.1:8080/, next free port if busy (PORT=9000 ./start.sh, NO_OPEN=1 ./start.sh)
```

Sidebar on the left lists every project page with what is missing or could be improved; the selected page opens in the viewport on the right (Desktop / Tablet / Phone width). Sites are listed in `overview/sites.json`, hand-written to-dos live in `overview/preview/todos.json`; checks like missing files, placeholders, screenshot and og:image are derived from each project's `docs/`. The preview serves the local stylesheet instead of the GitHub Pages one and strips the Umami script. Only the Python standard library, bound to 127.0.0.1.
