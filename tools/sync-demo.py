#!/usr/bin/env python3
"""Copies the built demo world (demo/dist/) into the projects.

Usage: python3 tools/sync-demo.py [--check] [id ...]   (default: all targets below)

Builds demo/dist/ first (demo/world.py build), then copies the files each project
needs to the place it reads them from. --check writes nothing and exits 1 if a
copy is missing or out of date (tools/check-demo.py is the same as --check).
Projects stay self-contained: they never read this repo at runtime.
"""
import filecmp
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO.parent
DIST = REPO / "demo" / "dist"

# id -> (project folder, [(file in demo/dist, target path in the project)])
TARGETS = {
    "kurrent": ("Kurrent", [("world.json", "demo/world.json")]),
    "plasmai": ("Plasmai", [("world.js", "contents/code/demoWorld.js")]),
    "framewidge": ("FrameWidge", [("world.json", "demo/world.json")]),
    "kimai-holiday": ("Kimai Holiday Plugin", [("world.json", "demo/world.json"), ("DemoWorld.php", "demo/DemoWorld.php")]),
    "kimai-abrechnung": ("Kimai Abrechnung", [("world.json", "demo/world.json"), ("DemoWorld.php", "demo/DemoWorld.php")]),
    "kimai-drehzettel": ("Kimai Drehzettel", [("world.json", "demo/world.json"), ("DemoWorld.php", "demo/DemoWorld.php")]),
    "kimai-anfahrten": ("Kimai Anfahrten", [("world.json", "demo/world.json"), ("DemoWorld.php", "demo/DemoWorld.php")]),
    "kimai-farbfaecher": ("Kimai Farbfächer", [("world.json", "demo/world.json"), ("DemoWorld.php", "demo/DemoWorld.php")]),
    "paperninja": ("PaperNinja", [("world.json", "app/demo/world.json")]),
    "papertty": ("PaperTTY", [("world.json", "demo/world.json")]),
    "dolphin-davinci": ("dolphin-davinci-audio-tools", [("world.json", "demo/world.json")]),
    "companion-mpris": ("companion/mpris", [("world.js", "src/demo/world.cjs")]),
    "kader": ("kader", [("world.json", "companion/demo/world.json")]),
    "andon": ("andon", [("world.json", "internal/services/seed/demo/world.json")]),
}
# The shared Kimai demo instance lives in this repo and reads demo/dist/ directly.


def main(argv):
    check = "--check" in argv
    ids = [a for a in argv if not a.startswith("--")] or list(TARGETS)
    unknown = [i for i in ids if i not in TARGETS]
    if unknown:
        sys.exit(f"unknown id: {', '.join(unknown)} (known: {', '.join(TARGETS)})")
    if not check:
        subprocess.run([sys.executable, str(REPO / "demo" / "world.py"), "build"], check=True)
    stale = 0
    for pid in ids:
        folder, files = TARGETS[pid]
        project = ROOT / folder
        if not project.is_dir():
            print(f"skip {pid}: {project} not found")
            continue
        for src_name, rel in files:
            src, dst = DIST / src_name, project / rel
            if dst.exists() and filecmp.cmp(src, dst, shallow=False):
                continue
            stale += 1
            if check:
                print(f"out of date: {folder}/{rel}")
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
                print(f"updated {folder}/{rel}")
    if check and stale:
        sys.exit(f"{stale} demo file(s) out of date, run tools/sync-demo.py")
    if not stale:
        print("demo world is up to date everywhere")


if __name__ == "__main__":
    main(sys.argv[1:])
