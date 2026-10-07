# Demo data: Studio Weber

Every shrippen project can start with the same made-up data, so screenshots look
consistent and never show real customers, people or files. `world/` is the single
source; `demo/tools/screenshots.py` takes the landing-page screenshots from it.

## The world

**Studio Weber** is a small film and sound studio in Hamburg-Ottensen, run by Mara Weber.
It likes to shoot at night: fog on the Elbe, harbour lights, beacons. Its work in Hamburg is
ordinary, but it leads to Graufeld (below), and a quiet thread runs under the ordinary data
(the hidden layer). Everything is fictional: people, companies, addresses, number plates, receipts. Mail
addresses use `example.test`, brands and products are invented.

| Person | Role | Kimai role | Shows up in |
|---|---|---|---|
| Mara Weber | Owner, producer | super admin | Plasmai, Kurrent, PaperNinja, Abrechnung, Anfahrten, andon |
| Jonas Brandt | Camera | user | Drehzettel (employed by Northlight for Harbour Lights), Anfahrten |
| Selin Aydın | Editing | user | Holiday (holidays), running timer |
| Theo Lindqvist | Sound and music | user | Holiday (sick days), score in companion-mpris, audio in dolphin |
| Lena Kraus | Production assistant | team lead | approvals in Holiday and Anfahrten |

| Customer | Project |
|---|---|
| Northlight Pictures (production company) | Harbour Lights – Season 2, a noir series in the port at night (episode 3 “Irrlicht”, 4 “Nebelhorn”, 5 “Drei Uhr dreizehn”) |
| Stiftung Elbfeuer (foundation for lighthouses and light vessels) | Image film “Feuer an der Elbe”, shot on a light vessel in HafenCity |
| Speiche Fahrradmanufaktur (bicycle maker) | Autumn spot “Licht an”: the lights go out, the dynamo light comes on |
| Studio Weber (internal) | Showreel 2026, Admin |
| Sendehaus Graufeld (regional broadcaster) | Nachtwache – miniseries |

Activities: shooting, pre-production, editing, sound mix, travel, meeting, bookkeeping.
Places are real Hamburg areas (Landungsbrücken, Övelgönne, HafenCity …) with made-up
street addresses. Media: the score *Harbour Lights (Original Score)* by Theo Lindqvist (Ebbe, Nebelhorn,
Leuchtfeuer, Drei Uhr dreizehn),
generated audio clips, synthetic film rolls, receipts from invented vendors. Suppliers the
studio pays regularly (`vendors`: mobile, hosting, software, energy, music) and its IT (`inventory`:
assets, licences, disks) are invented too; only the edit laptop is a real model, as in
FrameWidge.

### Graufeld

The second shooting area, about 110 km from the studio: fog, marsh and mud flats at the Elbe
mouth (`graufeld`, places `graufeld-lighthouse`, `kolk`, `moorhof`, `sendehaus`). The studio
shoots *Nachtwache* there for the Sendehaus Graufeld, a small regional broadcaster in an old
radio station: a crime writer (Ilva Brandes) vanishes, and her manuscript pages turn up
describing what has not happened yet. The Sendehaus runs a night programme, *Graufeld nach
Mitternacht*. Contact is Hinnerk Aalders, a retired lighthouse keeper. Fog warnings for the
shooting days are in `graufeld.weather`. Graufeld adds to the world; the Hamburg projects,
people and names stay as they are.

### IT documentation

`it_docs` is the studio's Obsidian vault for Hansei: three hosts named after Elbe sea marks
(Nebelhorn = the NAS, Feuerschiff = the rented Nordhost server, Boje = the Raspberry Pi),
service notes, a rulebook (`IT/Design.md`) and prepared review batches. Every Hansei check finds
something (a plain-text password and token, the old code names SW-NAS01/SW-VPS/SW-PI, a missing
frontmatter key, an old review date, a dead link, a compose copy). Dates are `{{day:N}}`
placeholders. The restore note mentions the returning file.

### The hidden layer

`oddities` is a quiet homage to Alan Wake, for the corners of a demo that few people read:
logs, backups, sensors, notes. Never explain it in the UI. The motif is **03:13 and seven
minutes**:

- manuscript pages found at the Landungsbrücken, in the studio, at the Moorhof and at the
  lighthouse, each describing something the data shows (the silent foghorn, the night
  recording that is too long, the detour on the way back, the light going out);
- the Sendehaus stream drops out every night at 03:13 for seven minutes (`night_outage`), and
  the lighthouse beacon flickers then (`flicker`);
- a deleted file comes back in the next backup (`returning_file`).

The same thread runs through ordinary data: the foghorn cue at 03:13 in Theo's score and
the track *Drei Uhr dreizehn*, the edit laptop rendering “the Kolk, night 3”, the terminal
listing `seite-7.pdf`, task t15 (a deleted file is back), Theo's night recording at the Kolk
(`nw_atmo_kolk_nacht3.m4a`, task t22), the return trip from the lighthouse that is 19 km
longer than the way there, receipt 11 (two floodlights, 40 batteries), task t23 (a manuscript
page on the edit desk that is not from the script).

Ids and the names that projects use in code or tests (people, Studio Weber, Northlight
Pictures, Harbour Lights, Speiche, the vendors, Elbstrand Övelgönne, the film rolls 03 and 04,
the van's plate) stay stable; change them only together with those projects. Texts
(timesheet descriptions, tasks, notes, tracks, the terminal) are free to change.

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
| `world/` | the source, edit this: one JSON file per topic (below), merged in `PARTS` order of `world.py`; a key lives in one file only |
| `world/it_docs/<lang>/` | the vault's notes as Markdown; `it_docs.json` lists their paths |
| `world.py` | `build` expands it into `dist/`; also a Python library (`World`) |
| `lib/world.js`, `lib/DemoWorld.php` | the same helpers for QML/Node and PHP |
| `dist/` | built files that `demo/tools/sync-demo.py` copies into the projects (committed) |
| `kimai/` | one Kimai instance with all plugins and the demo data |

### Topics

| File | Keys |
|---|---|
| `world.json` | studio, people (with working terms and commute), teams, time anchor, currency, password, `known_but_internal` |
| `business.json` | customers, projects, activities, film engagement (with pay terms), vendors, receipts, tasks; `bookkeeping` (the time and invoice scenario), `documents` (incl. the receipt scans), `assets_state`, `bank`, `subscriptions`, `suggestions`, `archive` (older projects with clashing colours), `approvals` |
| `time.json` | timesheet week templates, running timers, `standby_timer`, absences, public holidays |
| `travel.json` | places, vehicles, trips, rentals, `logbook` (how trips and rentals are booked), `location` (visits, track and one tracked day) |
| `it.json` | inventory, laptop (with its render job), terminal, speaker (with everything its web UI shows), dashboard; servers and services: `monitoring`, `server`, `virtualization`, `storage`, `disk_health`, `containers`, `stacks`, `backups`, `certs`, `domains`, `mail_blacklist`, `dns`, `gateway`, `vpn`, `tailnet`, `tunnel`, `speed`, `identity`, `passwords`, `cloud`, `downloads`, `code`, `json_api`, `heartbeats`, `prometheus`, `vulnerabilities`, `ci`, `backup_server`, `file_backups`, `image_updates` |
| `home.json` | `smart_home`, `pantry`, `kitchen`, `energy`, `weather` |
| `web.json` | `sites`, `feeds`, `bookmarks`, `mail`, `calendar` |
| `media.json` | the score, players, audio and video files, film rolls (`media`), `photos`, `library`, `series` |
| `story.json` | Graufeld, the hidden layer |
| `it_docs.json` | Hansei's vault: hosts, rules, batches, review and AI providers, the demo AI's script; note texts in `it_docs/<lang>/` |

Every section says what it is for in a `note` (left out of release samples). Service
sections describe what the studio's tools would report, with a story: something in each
needs attention, so dashboards and checks have something to show.

### Values

- `{"de": …, "en": …}`: a text in both languages; names stay plain strings.
- `"{{vendors.nordhost.name}}"`: a reference to another value, a list entry by its `id`
  (or index: `inventory.disks.0`). `world.py build` resolves it: alone it becomes the value
  itself (a number stays a number), inside a text its text; a text that embeds a `{de, en}`
  value becomes `{de, en}`. Name people, customers, vendors and projects this way, never by
  hand, so a rename reaches every place.
- `"@-3h"`, `"@+2d"`, `"@-1d6h"`: a time relative to now; `"@date-2"` a day relative to
  today (UTC), `"@date+0 09:05"` that day at a local time. For states that must look the
  same on every day of the week; the reader resolves them (Andon's `demoworld.Decode`). Plain
  day offsets from the anchor (below) are still the rule for the world's calendar.
- `{{day:N}}` in vault notes is the vault's own date placeholder.

After editing `world/`: `python3 demo/tools/sync-demo.py`, then commit the copies in the
projects. `python3 demo/tools/check-demo.py` reports stale copies.

## Starting a project with demo data

The demo is internal: it only exists to take screenshots and never ships (no option, command or
data in releases; each project's release build checks that).

| Project | Command |
|---|---|
| Kurrent | `demo/start.sh` (builds `build-demo/` with `-DKURRENT_DEMO=ON`, no Akonadi) |
| Plasmai | `demo/start.sh` (profile "Demo", in-memory Kimai) |
| FrameWidge | `demo/start.sh` (demo backend instead of framework-control) |
| Kimai plugins | `demo/start.sh [de\|en] [default\|knust]` (shared instance from `demo/kimai/`) |
| PaperNinja | `demo/start.sh` (the app has no demo code; `demo/run.py` wires it up) |
| kader | `demo/start.sh` (draws the rolls, then `kader open`) |
| companion-mpris | dev module entry `demo/main.js` (demo players; screenshot by hand) |
| dolphin-davinci-audio-tools | `demo/start.sh` (generated clips) |
| PaperTTY | `demo/start.sh` (renders the demo session with the Bitmap driver) |
| andon | `./start.sh demo` |
| Hansei | `demo/start.sh [de\|en] [tui]` (demo build, own vault from `it_docs`, scripted AI) |

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
