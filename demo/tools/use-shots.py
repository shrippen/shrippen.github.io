#!/usr/bin/env python3
"""Puts the demo screenshots (docs/shots/) into the landing pages (docs/index.html).

Usage: python3 demo/tools/use-shots.py [id ...] [--check]

Each project's demo/shots.json may have
  "page": {"old-image.jpg": "shot-name", ...}    images on the page to replace
  "page_theme": "default"                         which theme variant to use (Kimai plugins)
Every <img src="old-image.jpg" ...> becomes a pair that the language switch of Kante shows
one at a time: <img lang="en" src="shots/NAME-en.webp" ...><img lang="de" src="shots/NAME-de.webp" ...>
(one plain <img> when the project has only one language). Captions that still say "test data"
or "placeholder" are updated. --check only reports pages that still use a mapped old image.
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
ROOT = REPO.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
screenshots = __import__("screenshots")

CAPTION_FIXES = [
    (" (test data)", " (demo data)"), (" (Testdaten)", " (Demodaten)"), (" (earlier interface)", ""),
]
# Only inside figures and hero shots whose image was replaced:
PLACEHOLDER_FIXES = [("Placeholder graphic: ", ""), ("Placeholder: ", ""), ("Platzhalter: ", "")]
FIGURE = re.compile(r'<figure.*?</figure>|<div class="hero-shot">.*?</div>', re.S)


def shot_file(name, lang, theme, fmt):
    return f"shots/{name}-{lang}{'-' + theme if theme else ''}.{fmt}"


def rewrite(html, mapping, langs, theme, fmt, docs):
    missing = []
    for old, name in mapping.items():
        pattern = re.compile(r'<img(?P<before>[^>]*?)\ssrc="' + re.escape(old) + r'"(?P<after>[^>]*)>')
        files = {lang: shot_file(name, lang, theme, fmt) for lang in langs}
        missing += [f for f in files.values() if not (docs / f).exists()]

        def pair(m):
            if len(langs) == 1:
                return f'<img{m.group("before")} src="{files[langs[0]]}"{m.group("after")}>'
            return "".join(f'<img lang="{lang}"{m.group("before")} src="{files[lang]}"{m.group("after")}>'
                           for lang in langs)
        html = pattern.sub(pair, html)
    for a, b in CAPTION_FIXES:
        html = html.replace(a, b)

    def fix_figure(m):
        text = m.group(0)
        if 'src="shots/' in text:
            for a, b in PLACEHOLDER_FIXES:
                text = text.replace(a, b)
        return text
    return FIGURE.sub(fix_figure, html), missing


def main(argv):
    check = "--check" in argv
    ids = {a for a in argv if not a.startswith("--")}
    stale = 0
    for site, folder, m in screenshots.load_manifests(ids):
        if not m or "page" not in m:
            continue
        page = folder / "docs" / "index.html"
        html = page.read_text(encoding="utf-8")
        langs = m.get("langs", ["de", "en"])
        langs = sorted(langs, key=lambda l: l != "en")          # en first, like the page's text pairs
        themes = m.get("themes", [""])
        theme = m.get("page_theme", themes[0])
        new, missing = rewrite(html, m["page"], langs, theme, m.get("format", "webp"), folder / "docs")
        if missing:
            print(f"{site['id']}: missing {', '.join(missing)} (run demo/tools/screenshots.py {site['id']})")
            stale += 1
            continue
        if new == html:
            continue
        stale += 1
        if check:
            print(f"{site['id']}: page still uses old images")
        else:
            page.write_text(new, encoding="utf-8")
            print(f"{site['id']}: updated {page.relative_to(ROOT)}")
    if check and stale:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
