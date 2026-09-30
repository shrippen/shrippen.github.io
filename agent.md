# Working rules for this repository

## GUI rule

- Kante is the source of every shrippen GUI. Every project generates its GUI from Kante, not inspired by it; see [`kante/AGENT-RULE.md`](kante/AGENT-RULE.md) for the rule as it goes into each project's `agent.md`.
- A missing element is added here first (CSS or QML, README, catalogue in `kante/proposals`), then used by the projects. Do not let a project solve it locally.
- Kimai plugins are the exception: they use Knust (`shrippen/kimai-knust-bundle`), Kante's spinoff. Keep Knust's tokens, shapes and roles in step with Kante.
- No raw colours or fonts in `kante/css`; `kante/tools/check-tokens.py` enforces it.

## Working on Kante

- Run `./build.sh` after every change to `kante/` or `overview/projects.json` and commit the generated files in `docs/` and `kante/qml/Kante/` (`KantePalette.qml`, `qmldir`, `KantePlasmaButton.qml`).
- Tokens live in `kante/tokens/palette.json` and `variables.css`; they must match (`check-tokens.py`).
- New motion goes into the `prefers-reduced-motion: no-preference` block at the end of `components.css` and follows `KanteStyle.motion` in QML.
- Every new QML component gets a test in `kante/qml/tests` and an entry in `kante/qml/demo/Gallery.qml`.
