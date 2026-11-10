# Working rules for this repository

The rules for all shrippen repositories are in `RULES.md` (writing, code, commits, bug
fixes, repository). It is a synced copy from the rules repository; do not edit it
here. This file holds only what is particular to this repository. A Claude Code session on
the owner's machine has the rules through the global `CLAUDE.md` already.

## What lives here

- The overview page (`overview/`, built into `docs/index.html`) and the shared demo world and screenshot tools (`demo/`).
- Kante, Knust and the Kimai plugin kit live in their own repository, [shrippen/Kante](https://github.com/shrippen/Kante) (checkout `../Kante`). Design changes go there, never into `docs/v1/` here; see Kante's `agent.md` and `AGENT-RULE.md`.
- `./build.sh` copies `../Kante/docs/v1/` unchanged into `docs/v1/` (served at `https://shrippen.github.io/v1/`, linked by every landing page) and builds the overview. Run it after every change to Kante, `overview/projects.json` or `overview/sites.json` and commit `docs/`.

## Release rule (all projects)

- Every release gets a detailed release log with graphics: a lead, the changes grouped as New, Improved, Fixed and Note, each point with what changed for the user and why; a demo screenshot per visible change (every language of the page), a diagram for changes inside.
- The log goes into the release notes on Gitea and as the newest entry of `#changes` on the project's landing page (Kante `.changelog`, 1.17). A release is done when the landing page shows it. Details: `overview/PROJECTS.md`.

## Repository (this project)

- Claude may merge its own PRs on Gitea after a clean `./build.sh` (this repository has no CI; decision G-07 in Kaiwa) and the Claude review leaves no **Wichtig** open (see the skill `pr-review`). A PR that changes `demo/` also needs `python3 demo/world.py build` without a diff in `demo/dist/` and a clean `python3 demo/tools/check-demo.py` (its "skip" lines do not count as clean), or the PR names the projects that follow and the skipped ones (`REVIEW.md`).
- Everything else: `RULES.md` (Repository) and the skill `pr-review`.
