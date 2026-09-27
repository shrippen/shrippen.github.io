# Demo data: Studio Weber

Every shrippen project can start with the same made-up data, so screenshots look
consistent and never show real customers, people or files. `world.json` is the single
source; `demo/tools/screenshots.py` takes the landing-page screenshots from it.

## The world

**Studio Weber** is a small film and media studio in Hamburg-Ottensen, run by Mara Weber.
Everything is fictional: people, companies, addresses, number plates, receipts. Mail
addresses use `example.test`, brands and products are invented.

| Person | Role | Kimai role | Shows up in |
|---|---|---|---|
| Mara Weber | Owner, producer | super admin | Plasmai, Kurrent, PaperNinja, Abrechnung, Anfahrten, andon |
| Jonas Brandt | Camera | user | Drehzettel (employed by Northlight for Harbour Lights), Anfahrten |
| Selin Aydın | Editing | user | Holiday (holidays), running timer |
| Theo Lindqvist | Sound | user | Holiday (sick days), score in companion-mpris, audio in dolphin |
| Lena Kraus | Production assistant | team lead | approvals in Holiday and Anfahrten |

| Customer | Project |
|---|---|
| Northlight Pictures (production company) | Harbour Lights – Season 2 (TV series) |
| Elbgrün Stiftung (foundation) | Tidenhub image film |
| Speiche Fahrradmanufaktur (bicycle maker) | Spring commercial |
| Studio Weber (internal) | Showreel 2026, Admin |

Activities: shooting, pre-production, editing, sound mix, travel, meeting, bookkeeping.
Places are real Hamburg areas (Landungsbrücken, Övelgönne, HafenCity …) with made-up
street addresses. Media: the score *Harbour Lights (Original Score)* by Theo Lindqvist,
generated audio clips, synthetic film rolls, receipts from invented vendors.

Colours come from the Kante palette. Kimai Farbfächer uses `clash_color` instead, so its
demo has the colour clashes the plugin is there to fix.

## Time

Every date is a **day offset** from the anchor, the Monday of the week that contains
*today*. `DEMO_TODAY=YYYY-MM-DD` fixes today; without it the real date is used, so a demo
started on any day looks current. Screenshots use `screenshot_today` (a Wednesday) so
they come out the same on every run.

Timesheets are written as week templates per person (`timesheet_weeks`) and expanded by
`world.py build`. Days with an approved absence are skipped; rows after *now* and rows
that overlap a running timer are dropped at runtime (`pastTimesheets`). Public holidays
are real dates (Hamburg, 2025–2027).

## Language

Names stay the same in both languages; every other text is `{"de": …, "en": …}`.
Screenshots are taken once per language.

## Files

| File | What |
|---|---|
| `world.json` | the source, edit this |
| `world.py` | `build` expands it into `dist/`; also a Python library (`World`) |
| `lib/world.js`, `lib/DemoWorld.php` | the same helpers for QML/Node and PHP |
| `dist/` | built files that `demo/tools/sync-demo.py` copies into the projects (committed) |
| `kimai/` | one Kimai instance with all plugins and the demo data |

After editing `world.json`: `python3 demo/tools/sync-demo.py`, then commit the copies in the
projects. `python3 demo/tools/check-demo.py` reports stale copies.

## Starting a project with demo data

| Project | Command |
|---|---|
| Kurrent | `demo/start.sh` (`KURRENT_DEMO=1`, no Akonadi) |
| Plasmai | `demo/start.sh` (profile "Demo", in-memory Kimai) |
| FrameWidge | `demo/start.sh` (demo backend instead of framework-control) |
| Kimai plugins | `demo/start.sh [de\|en] [default\|knust]` (shared instance from `demo/kimai/`) |
| PaperNinja | `./start.sh demo` |
| kader | `kader demo` |
| companion-mpris | `demo/start.sh` (`MPRIS_DEMO=1`, Companion in Docker) |
| dolphin-davinci-audio-tools | `demo/start.sh` (generated clips) |
| PaperTTY | `demo/start.sh` (renders the demo session with the Bitmap driver) |
| andon | `./start.sh demo` |

## Screenshots

```sh
python3 -m venv demo/tools/.venv && demo/tools/.venv/bin/pip install playwright pillow   # once
demo/tools/.venv/bin/python demo/tools/screenshots.py              # all projects, de + en
demo/tools/.venv/bin/python demo/tools/screenshots.py kurrent --lang en
demo/tools/.venv/bin/python demo/tools/screenshots.py --list
```

Each project lists its shots in `demo/shots.json` (format in the docstring of
`demo/tools/screenshots.py`). Images go to `<project>/docs/shots/<name>-<lang>[-<theme>].webp`;
`demo/tools/use-shots.py` puts them into the landing pages (the `page` map in `shots.json`).

How the shots are taken:

- **Web apps** (PaperNinja, kader, andon, Kimai plugins): Playwright with `/usr/bin/chromium`.
  The Kimai plugins share one run per language and theme (`default` and `knust`).
- **Plasma widgets** (Kurrent, Plasmai, FrameWidge): offscreen `plasmoidviewer` with a scratch
  config home; the widget grabs itself with `grabToImage` (Kurrent through `tests/screenshot.sh`,
  Plasmai and FrameWidge through a `ScreenshotRunner.qml` that only acts when a plan is present).
- **PaperTTY**: the real Bitmap driver renders the demo session, drawn into an e-ink panel.
- **By hand** (listed as `manual`): the Dolphin context menu and progress dialog (native KDE
  windows; `demo/start.sh convert` prepares them) and the Companion button page (the module does
  not start as a dev module in Companion 5.0.6 in Docker; the demo mode itself works).

Apps on the real clock (Kimai, Kurrent, Plasmai, andon) place the data around the real today;
the others use `screenshot_today`.

## Not included

**Kintsugi** is known but stays internal for the foreseeable future, so it has no demo
data and no screenshots. Rakugo has no UI; lmix and Public Arcade are not covered yet.
