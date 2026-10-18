# Review guide

Every PR is reviewed by a new Claude agent before it is merged (rule in
`agent.md`, owner 18.10.2026). The agent knows nothing of the session that
wrote the change: it gets the PR's intent, its diff and the repository, and
this file. The owner does not read code; this review is the second reader.

## What failure looks like here

This repository serves `https://shrippen.github.io/` (overview page and
Kante's `v1/` build, linked by every landing page) and the demo world that
every project's screenshots come from. A bug that matters is one a visitor
or another project notices:

- **Site breaks:** `docs/v1/` is not Kante's build unchanged, so
  `shrippen.css` / `shrippen.js` break every landing page; a dead link,
  missing icon or wrong page URL on the overview; a text in only one
  language (`lang="en"` / `lang="de"` pairs).
- **Demo world breaks a project:** an id or a name that projects use in
  code or tests (people, Studio Weber, Northlight, Harbour Lights, vendors,
  film rolls, the van's plate) changes without those projects; a
  `{{path}}` reference that does not resolve; a `{de, en}` text missing
  one side; a date that is not a day offset from the anchor; a key in two
  `world/` files; `dist/` not rebuilt.
- **Leaks the real:** a real person, customer, address, mail (only
  `example.test`) or brand in the demo world or a screenshot.
- **Update checks lie:** `docs/versions.json` lists a draft, a
  pre-release or a wrong version or URL (format in `overview/VERSIONS.md`).
- **Lies:** docs or comments that say what the code does not do.

## What to check in particular

- Kante rule: no design change in `docs/v1/` or in the overview's own
  styles; a missing element goes into Kante first. The overview uses
  Kante's roles, no raw colours or fonts (`check-tokens.py` in `build.sh`).
- `docs/` matches its sources: after a change to `overview/projects.json`
  or to Kante, `./build.sh` ran and `docs/` is committed; after a change
  to `demo/world/`, `demo/dist/` is rebuilt (`world.py build`).
- Release rule: a release log on a landing page has a lead, New /
  Improved / Fixed / Note, a screenshot per visible change in every
  language (details in `overview/PROJECTS.md`).
- `world.py`, `lib/world.js` and `lib/DemoWorld.php` keep the same
  runtime rules; the preview server stays bound to 127.0.0.1.

## Skip

- Generated files: `docs/v1/` (Kante's build), `docs/index.html`,
  `docs/assets/icons/`, `demo/dist/` (only check that they were rebuilt).
- Screenshots and images (`docs/social-preview.png`).

## How to report

- Every finding names file and line and the concrete input or state that
  goes wrong. No guess without evidence; if unsure, say so.
- Each finding gets one label: **Wichtig** (a bug from the list above,
  must be fixed or answered before the merge), **Kleinigkeit** (optional,
  at most five) or **Bestand** (the bug was there before this PR; not
  blocking).
- The report starts with the count, e.g. "2 Wichtig, 1 Kleinigkeit" (the
  session puts the heading above it). The count of **Wichtig** holds every
  one still open, also from an earlier round, e.g. "1 Wichtig (offen aus
  Runde 1)". Only when none is open it says plainly: "Nichts zu beheben."
- In a later round: say for each open **Wichtig** of the last round whether
  it is fixed, or whether its answer is accepted, with the reason.
- Findings in German, code names as they are.
