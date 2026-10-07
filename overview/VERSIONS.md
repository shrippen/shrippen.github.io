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

Wherever nothing else announces updates:

| Gets the hint | No hint (the platform announces updates) |
|---|---|
| Kimai plugins (installed by copying) | Flathub, F-Droid, app stores |
| Docker images (`docker pull` says nothing by itself) | KDE Store (Discover), AUR |
| AppImage, Windows `.exe`, tarballs, `pip`/`install.sh` installs | HACS, Home Assistant add-ons |
| self-built releases, device packages | |

One project often has both kinds of build; the check is a build switch that the store builds leave out (checked like the demo exclusion).

## Clients

| Client | Where it runs | Shows |
|---|---|---|
| `kit.update_hint` (Kante kit 0.8) | Kimai, in the admin's browser | kit hint card |
| `KanteUpdateCheck` (Kante 1.22) | Qt Quick / Kirigami apps, Plasmoids | `KanteCallout` |
| server side, own code | self-hosted web apps (Docker, device daemons, local web UIs) | Kante `.callout.has-x` |

**Server side:** a web app with a Content-Security-Policy (`connect-src 'self'`) must not fetch from the browser, so its backend asks instead: at most once a day, cached in its data folder, silent on failure, the same comparison and checks as above (format 1, `https` links). It shows the hint only to admins, as a dismissible callout with a link (`<div class="callout has-x">` with `.callout-x`, Kante README); dismissing hides it until the next version.

Rules for every client:

- at most one request per project per day; failures stay silent
- a plain GET of `versions.json`: no parameters, no cookies, nothing that identifies a user or an installation
- only a hint with a link; never downloads or installs anything
- can be switched off, and the README says what is fetched from where
- off in demo mode (no network access there)

## No counting

The update check counts nothing and sends nothing back. How often a project is used is read from the download counts of the releases (Gitea, GitHub, KDE Store).
