# Demo data: Studio Weber

Every shrippen project can start with the same made-up data, so screenshots look
consistent and never show real customers, people or files. `world.json` is the single
source; `tools/screenshots.py` takes the landing-page screenshots from it.

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
| `dist/` | built files that `tools/sync-demo.py` copies into the projects (committed) |
| `kimai/` | one Kimai instance with all plugins and the demo data |

After editing `world.json`: `python3 tools/sync-demo.py`, then commit the copies in the
projects. `python3 tools/check-demo.py` reports stale copies.

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
python3 -m venv tools/.venv && tools/.venv/bin/pip install playwright pillow   # once
tools/.venv/bin/python tools/screenshots.py              # all projects, de + en
tools/.venv/bin/python tools/screenshots.py kurrent --lang en
tools/.venv/bin/python tools/screenshots.py --list
```

Each project lists its shots in `demo/shots.json` (format in the docstring of
`tools/screenshots.py`). Images go to `<project>/docs/shots/<name>-<lang>[-<theme>].webp`.

## Not included

**Kintsugi** is known but stays internal for the foreseeable future, so it has no demo
data and no screenshots. Rakugo has no UI; lmix and Public Arcade are not covered yet.
