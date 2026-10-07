#!/usr/bin/env python3
"""Builds docs/versions.json: the latest release of every project, read by the update checks.

For each project in overview/sites.json whose folder sits next to this repo and whose `origin`
is on git.arianw.de, asks Gitea for the latest release (no drafts, no pre-releases) through
`tea api` (login git.arianw.de) and links the release page on the GitHub mirror, because the
Gitea repos are not public. Warns when the mirror does not have the release yet.
Format and clients: overview/VERSIONS.md.
Usage: python3 overview/tools/build-versions.py   (after tagging a release; needs tea and network)
"""
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

OVERVIEW = Path(__file__).resolve().parent.parent
REPO = OVERVIEW.parent
ROOT = REPO.parent
OUT = REPO / "docs" / "versions.json"
GITHUB = "https://github.com/shrippen"
GITEA = "https://git.arianw.de/"
FORMAT = 1


def gitea_repo(folder):
    try:
        url = subprocess.run(["git", "-C", str(folder), "remote", "get-url", "origin"],
                             capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    if not url.startswith(GITEA):
        return None
    return url[len(GITEA):].removesuffix(".git")


def latest_release(repo):
    result = subprocess.run(["tea", "api", "--login", "git.arianw.de", f"/repos/{repo}/releases/latest"],
                            capture_output=True, text=True, cwd=REPO)
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None
    if "tag_name" not in data or data.get("draft") or data.get("prerelease"):
        return None
    return data


def on_mirror(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=10) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError):
        return False


def main():
    projects = {}
    for site in json.loads((OVERVIEW / "sites.json").read_text(encoding="utf-8")):
        # same rule as build-overview.py; a page inside another repo ("repo" with a path) has no own releases
        github = site.get("repo") or site["url"].split("shrippen.github.io/", 1)[1].split("/", 1)[0]
        if not github or "/" in github:
            continue
        repo = gitea_repo(ROOT / site["dir"])
        if repo is None:
            continue
        release = latest_release(repo)
        if release is None:
            continue
        tag = release["tag_name"]
        url = f"{GITHUB}/{github}/releases/tag/{tag}"
        if not on_mirror(url):
            print(f"warning: {site['id']} {tag} is not on the GitHub mirror yet: {url}", file=sys.stderr)
        projects[site["id"]] = {
            "version": tag.removeprefix("v"),
            "date": release["published_at"][:10],
            "url": url,
        }
    data = {"format": FORMAT, "projects": dict(sorted(projects.items()))}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({len(projects)} projects)")


if __name__ == "__main__":
    main()
