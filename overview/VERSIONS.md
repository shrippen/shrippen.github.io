# versions.json: update checks

`docs/versions.json` (served at <https://shrippen.github.io/versions.json>) lists the latest release of every project. The update checks in the Kimai plugin kit (`kit.update_hint`) and in Kante QML (`KanteUpdateCheck`) read it and show a hint with a link when a newer version exists. They never download or install anything.

## Format

```json
{
  "format": 1,
  "projects": {
    "kimai-anfahrten": {
      "version": "0.10.0",
      "date": "2026-10-05",
      "url": "https://github.com/shrippen/kimai-anfahrten/releases/tag/v0.10.0"
    }
  }
}
```

| Field | Meaning |
|---|---|
| `format` | version of this format. Clients ignore files with a `format` they do not know (newer clients read 1 as long as it exists). A new optional field does not change it; removing or redefining one does |
| `projects` | key = project id from `overview/sites.json` |
| `version` | tag of the latest release without a leading `v`; no drafts, no pre-releases |
| `date` | release date, `YYYY-MM-DD` |
| `url` | release page on the GitHub mirror (the Gitea repos are not public) |

Comparison: the parts of `version` separated by `.` are compared as numbers (`0.10.0` > `0.9.3`), missing parts count as 0, anything after `-` or `+` is ignored. A client shows the hint only when `version` is greater than its own.

## Building

```bash
python3 overview/tools/build-versions.py   # needs tea (login git.arianw.de) and network
```

Run it after tagging a release and commit `docs/versions.json` with the release's landing-page update. It reads the latest Gitea release of each project in `sites.json` whose folder sits next to this repo and warns when the GitHub mirror does not have the release yet. `./build.sh` does not run it, because it needs the network and a Gitea login.

## Where a project uses it

Only where nothing else announces updates: Kimai plugins (installed by copying), tarballs, AppImages, self-built releases. Not for builds from F-Droid, Flathub, the AUR or the KDE Store (Discover); there the package manager is in charge and a project leaves the check out of that build.

Rules for every client:

- at most one request per project per day; failures stay silent
- a plain GET of `versions.json`: no parameters, no cookies, nothing that identifies a user or an installation
- can be switched off, and the README says what is sent where
- off in demo mode (no network access there)

## No counting

The update check counts nothing and sends nothing back. How often a project is used is read from the download counts of the releases (Gitea, GitHub, KDE Store).
