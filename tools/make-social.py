#!/usr/bin/env python3
"""Renders docs/social-preview.png (1280x640) for every project from its docs/icon.svg.

Usage: python3 tools/make-social.py [id ...]   (ids from preview/sites.json; default: all)
Needs chromium. Layout follows the README: dark card, colour logo, name, tagline, bottom strip.
"""
import json
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO.parent
WIDTH, HEIGHT = 1280, 640
LOGO_PX = 144
MAX_TITLE_PX = 76
TITLE_BUDGET_PX = 1080
CHAR_WIDTH = 0.6  # rough Rajdhani caps advance incl. letter-spacing, in em

# id -> (title, tagline)
COPY = {
    "overview": ("shrippen", "Open-source tools for KDE Plasma, Kimai and the desktop"),
    "kurrent": ("Kurrent", "A KDE Plasma 6 task manager"),
    "plasmai": ("Plasmai", "Time tracking for KDE Plasma"),
    "papertty": ("PaperTTY", "Linux terminal on e-ink"),
    "framewidge": ("FrameWidge", "KDE widget for Framework laptops"),
    "paperninja": ("PaperNinja", "Match expenses with receipts"),
    "dolphin-davinci": ("Dolphin Davinci Audio Tools", "Audio and video tools for Davinci Resolve"),
    "kimai-holiday": ("Working Hours & Holidays", "Kimai plugin for working hours and holidays"),
    "companion-mpris": ("Companion MPRIS", "Media player control for Bitfocus Companion"),
    "kader": ("Kader", "Crops film negative scans to the frame"),
    "kimai-abrechnung": ("Kimai Abrechnung", "Billing overview for Kimai"),
    "kimai-drehzettel": ("Drehzettel", "Film crew timesheets for Kimai"),
    "kimai-anfahrten": ("Anfahrten", "Trips and travel costs for Kimai"),
}


def card(title, tagline, repo, logo):
    size = min(MAX_TITLE_PX, int(TITLE_BUDGET_PX / (len(title) * CHAR_WIDTH)))
    fonts = REPO / "fonts"
    return f"""<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:R;font-weight:700;src:url(file://{fonts}/Rajdhani-700.ttf)}}
@font-face{{font-family:M;font-weight:400;src:url(file://{fonts}/JetBrainsMono-400.ttf)}}
*{{margin:0;box-sizing:border-box}}
body{{width:{WIDTH}px;height:{HEIGHT}px;background:#1d2021;position:relative;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:26px;padding-bottom:64px}}
img{{width:{LOGO_PX}px;height:{LOGO_PX}px}}
h1{{font:700 {size}px/1 R;letter-spacing:.12em;text-transform:uppercase;color:#fbf1c7;text-align:center}}
p{{font:400 26px/1.3 -apple-system,'Segoe UI',Roboto,'DejaVu Sans',sans-serif;color:#d5c4a1;text-align:center}}
.line{{position:absolute;left:0;right:0;top:580px;height:1px;background:#504945}}
.foot{{position:absolute;left:0;right:0;top:596px;text-align:center;font:400 18px/1 M;letter-spacing:.06em;color:#a89984}}
</style>
<img src="file://{logo}" alt="">
<h1>{escape(title)}</h1>
<p>{escape(tagline)}</p>
<div class="line"></div>
<div class="foot">github.com/shrippen/{escape(repo)}</div>"""


def render(site):
    docs = ROOT / site["dir"] / "docs"
    logo = docs / "icon.svg"
    if not logo.exists():
        print(f"skip {site['id']}: no docs/icon.svg")
        return
    title, tagline = COPY[site["id"]]
    repo = site["url"].rstrip("/").rsplit("/", 1)[-1]
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "card.html"
        page.write_text(card(title, tagline, repo, logo), encoding="utf-8")
        out = docs / "social-preview.png"
        subprocess.run(
            ["chromium", "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
             "--force-device-scale-factor=1", f"--window-size={WIDTH},{HEIGHT}",
             "--virtual-time-budget=3000", f"--screenshot={out}", f"file://{page}"],
            check=True, capture_output=True)
    print(f"{site['id']:22} -> {out.relative_to(ROOT)}")


def main():
    sites = json.loads((REPO / "preview" / "sites.json").read_text(encoding="utf-8"))
    wanted = set(sys.argv[1:])
    for site in sites:
        if not wanted or site["id"] in wanted:
            render(site)


if __name__ == "__main__":
    main()
