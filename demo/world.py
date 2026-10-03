#!/usr/bin/env python3
"""Studio Weber, the shared demo world of all shrippen projects.

demo/world/ is the source: one file per topic, merged in PARTS order ({{path}}
references resolved, see resolve()), and the
IT vault as Markdown (world/it_docs/<lang>/<path>). `python3 demo/world.py build`
merges and expands it into
demo/dist/world.json (plus world.js with the data embedded, for QML and Node,
and DemoWorld.php), which demo/tools/sync-demo.py copies into every project:
the week templates become one row per timesheet, so no project has to repeat
that logic. Every date in the built file is still a day offset from the anchor.

Runtime rules (the same in world.js and DemoWorld.php):
  today  = DEMO_TODAY (YYYY-MM-DD) if set, else the real date
  anchor = Monday of the week that contains today
  date   = anchor + offset days
  text   = value[lang] if value is a {de, en} dict, else value

This module also works as a library: `from world import World`.
"""
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "world"
# Topic files of the source, merged in this order; a key may appear in one only.
#   world     studio, people, teams, time anchor      business  customers, projects, receipts, tasks
#   time      timesheets, absences, holidays          travel    places, vehicles, trips
#   it        devices, hosts, services, network       home      smart home, kitchen, energy
#   web       sites, feeds, links, mail               media     music, photos, library
#   story     Graufeld, the hidden layer              it_docs   Hansei's vault (texts in it_docs/)
PARTS = ("world", "business", "time", "travel", "it", "home", "web", "media", "story", "it_docs")
VAULT = SOURCE / "it_docs"
DIST = HERE / "dist" / "world.json"
LANGS = ("de", "en")


def today():
    raw = os.environ.get("DEMO_TODAY", "").strip()
    return dt.date.fromisoformat(raw) if raw else dt.date.today()


def anchor(day=None):
    day = day or today()
    return day - dt.timedelta(days=day.weekday())


def text(value, lang):
    if isinstance(value, dict) and set(value) <= set(LANGS) and value:
        return value.get(lang) or value.get("en") or ""
    return value


def _minutes(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def expand_timesheets(world):
    """One row per timesheet: {id, user, project, activity, day, start, end, description, exported}."""
    spec = world["timesheet_weeks"]
    absent = {}
    for a in world["absences"]:
        if a["status"] == "approved":
            for d in range(a["from"], a["to"] + 1):
                absent.setdefault(a["user"], set()).add(d)
    billable = {p["id"]: p["billable"] for p in world["projects"]}
    rows = []
    for user, templates in spec["templates"].items():
        for week in range(spec["from_week"], spec["to_week"] + 1):
            for weekday, project, activity, start, end, desc in templates[week % len(templates)]:
                day = week * 7 + weekday
                if day in absent.get(user, ()):
                    continue
                rows.append({
                    "user": user, "project": project, "activity": activity, "day": day,
                    "start": start, "end": end, "description": desc,
                    "exported": billable[project] and day < spec["exported_before_day"],
                })
    rows.sort(key=lambda r: (r["day"], _minutes(r["start"]), r["user"]))
    for i, r in enumerate(rows, 1):
        r["id"] = i
    return rows


def vault_text(path):
    """A vault note's {de, en} text from world/it_docs/<lang>/<path>."""
    return {lang: (VAULT / lang / path).read_text(encoding="utf-8") for lang in LANGS if (VAULT / lang / path).exists()}


def load():
    """The source as one dict: topic files merged, vault texts filled in."""
    world = {}
    for part in PARTS:
        file = SOURCE / f"{part}.json"
        if not file.exists():
            continue
        data = json.loads(file.read_text(encoding="utf-8"))
        twice = set(world) & set(data)
        assert not twice, f"{file.name}: {sorted(twice)} already defined"
        world.update(data)
    docs = world.get("it_docs", {})
    for entry in docs.get("notes", []) + docs.get("private", []) + [docs[k] for k in ("rulebook", "agent") if k in docs]:
        entry["content"] = vault_text(entry["path"])
        assert entry["content"], f"no vault text for {entry['path']}"
    return world


REF = re.compile(r"\{\{([a-z_]+(?:\.[A-Za-z0-9_-]+)+)\}\}")


def lookup(world, path):
    """A value by dotted path; in a list a key is an entry's id, else its index."""
    node = world
    for key in path.split("."):
        if isinstance(node, dict):
            node = node[key]
        else:
            hit = [x for x in node if isinstance(x, dict) and str(x.get("id")) == key]
            node = hit[0] if hit else node[int(key)]
    return node


def resolve(world, node, lang=None):
    """Replaces {{path}} references: alone the value itself, inside a text its text. A text
    that embeds a {de, en} value becomes {de, en} itself."""
    if isinstance(node, dict):
        if node and set(node) <= set(LANGS):
            return {k: resolve(world, v, k) for k, v in node.items()}
        return {k: resolve(world, v, lang) for k, v in node.items()}
    if isinstance(node, list):
        return [resolve(world, v, lang) for v in node]
    if not isinstance(node, str) or "{{" not in node:
        return node
    whole = REF.fullmatch(node)
    if whole:
        return resolve(world, lookup(world, whole.group(1)), lang)
    if lang is None and any(isinstance(lookup(world, m), dict) and set(lookup(world, m)) <= set(LANGS) for m in REF.findall(node)):
        return {l: resolve(world, node, l) for l in LANGS}
    return REF.sub(lambda m: str(text(resolve(world, lookup(world, m.group(1)), lang), lang or "de")), node)


def build():
    world = load()
    world = resolve(world, world)
    ids = {kind: {x["id"] for x in world[kind]} for kind in ("people", "customers", "projects", "activities")}
    world["timesheets"] = expand_timesheets(world)
    for r in world["timesheets"] + world["running"]:
        assert r["user"] in ids["people"], r
        assert r["project"] in ids["projects"], r
        assert r["activity"] in ids["activities"], r
    for p in world["projects"]:
        assert p["customer"] in ids["customers"], p
    DIST.parent.mkdir(exist_ok=True)
    DIST.write_text(json.dumps(world, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    js = (HERE / "lib" / "world.js").read_text(encoding="utf-8")
    (DIST.parent / "world.js").write_text(
        "// Generated by demo/world.py from demo/world/. Do not edit.\n"
        f"var WORLD_DATA = {json.dumps(world, ensure_ascii=False)};\n\n{js}", encoding="utf-8")
    (DIST.parent / "DemoWorld.php").write_text((HERE / "lib" / "DemoWorld.php").read_text(encoding="utf-8"), encoding="utf-8")
    return world


class World:
    """Built world with resolved dates and texts for one language."""

    def __init__(self, lang="de", path=DIST, day=None):
        self.data = json.loads(Path(path).read_text(encoding="utf-8"))
        self.lang = lang
        self.today = day or today()
        self.anchor = anchor(self.today)
        self.today_offset = (self.today - self.anchor).days

    def date(self, offset):
        return self.anchor + dt.timedelta(days=offset)

    def t(self, value):
        return text(value, self.lang)

    def by_id(self, kind):
        return {x["id"]: x for x in self.data[kind]}

    def past_timesheets(self, now=None):
        """Timesheets up to now, without the ones that would overlap a running timer."""
        now = now or dt.datetime.now().strftime("%H:%M")
        running = {r["user"]: r["start"] for r in self.data["running"]}
        out = []
        for r in self.data["timesheets"]:
            if r["day"] > self.today_offset:
                continue
            if r["day"] == self.today_offset:
                limit = running.get(r["user"], now)
                if _minutes(r["end"]) > _minutes(min(limit, now)):
                    continue
            out.append(r)
        return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        w = build()
        print(f"built {DIST.relative_to(HERE.parent)}: {len(w['timesheets'])} timesheets, "
              f"{len(w['tasks']['items'])} tasks, {len(w['receipts'])} receipts")
    elif cmd == "dates":
        w = World(sys.argv[2] if len(sys.argv) > 2 else "de")
        print(f"today {w.today} (offset {w.today_offset}), anchor {w.anchor}")
    else:
        sys.exit(__doc__)
