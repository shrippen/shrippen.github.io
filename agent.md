# Working rules for this repository

## What lives here

- The overview page (`overview/`, built into `docs/index.html`) and the shared demo world and screenshot tools (`demo/`).
- Kante, Knust and the Kimai plugin kit live in their own repository, [shrippen/Kante](https://github.com/shrippen/Kante) (checkout `../Kante`). Design changes go there, never into `docs/v1/` here; see Kante's `agent.md` and `AGENT-RULE.md`.
- `./build.sh` copies `../Kante/docs/v1/` unchanged into `docs/v1/` (served at `https://shrippen.github.io/v1/`, linked by every landing page) and builds the overview. Run it after every change to Kante or to `overview/projects.json` and commit `docs/`.

## Repository rule

- This repository lives on Gitea (`git.arianw.de`). GitHub is only a push mirror of it.
- Changes arrive as pull requests: work on a branch, open a PR, merge it on Gitea (the mirror follows).
- Never merge a PR, push to `main` (or any default branch), push tags or publish releases on GitHub. A merge there is overwritten by the next Gitea push.
- Never force-push a branch that someone else's PR depends on.
