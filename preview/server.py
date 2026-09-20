#!/usr/bin/env python3
"""Local preview of all project landing pages.

Serves each project's docs/ folder under /site/<id>/, the central stylesheet
from this repo under /dd/, and a sidebar UI at /. Only the standard library.
"""
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PROJECTS_ROOT = REPO.parent
HOST = "127.0.0.1"
START_PORT = int(os.environ.get("PORT", "8080"))
MAX_PORT_TRIES = 100

CENTRAL_BASE = "https://shrippen.github.io/DesignDefault/v1/"
LOCAL_BASE = "/dd/v1/"
UMAMI_TAG = re.compile(r"<script[^>]*um\.arianw\.de[^>]*></script>\s*")
LARGE_IMAGE_BYTES = 800 * 1024
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
NO_SCREENSHOT = "No screenshot on the page"
PLACEHOLDER = re.compile(r"\[(?:INSTALL|LICENSE|LIZENZ|VERSION)[^\]]*\]|PROJECT_[A-Z_]+")


def load_json(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def docs_dir(site):
    return PROJECTS_ROOT / site["dir"] / "docs"


def git_out(site, *args):
    cmd = ["git", "-C", str(PROJECTS_ROOT / site["dir"]), *args]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=5).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def auto_todos(site):
    """Checks that can be derived from the files themselves."""
    docs = docs_dir(site)
    index = docs / "index.html"
    if not index.exists():
        return [{"level": "missing", "text": "No docs/index.html", "auto": True}]

    html = index.read_text(encoding="utf-8")
    todos = []

    def add(level, text):
        todos.append({"level": level, "text": text, "auto": True})

    refs = re.findall(r'(?:src|href)="([^"#?]+)"', html)
    local = [r for r in refs if not re.match(r"^(https?:|mailto:|//|data:)", r)]
    missing = sorted({r for r in local if not (docs / r).exists()})
    if missing:
        add("missing", "Referenced file not in docs/: " + ", ".join(missing))

    fav = re.search(r'<link rel="icon" href="([^"]+)"', html)
    if not fav:
        add("missing", "No favicon / logo referenced")

    if not (docs / "icon-mono.svg").exists():
        add("improve", "No monochrome logo (icon-mono.svg)")

    if 'class="hero-shot"' not in html and 'class="shots"' not in html:
        add("missing", NO_SCREENSHOT)

    og = re.search(r'property="og:image" content="([^"]+)"', html)
    if not og:
        add("improve", "No og:image (social preview)")
    elif not (docs / og.group(1).rsplit("/", 1)[-1]).exists():
        add("missing", "og:image file not found in docs/: " + og.group(1).rsplit("/", 1)[-1])

    left = sorted(set(PLACEHOLDER.findall(html)))
    if left:
        add("missing", "Placeholders left in page: " + ", ".join(left))

    files = [p for p in docs.rglob("*") if p.is_file() and p != index]
    unused = sorted(p.name for p in files if p.name not in html and p.name != "icon-mono.svg")
    if unused:
        add("info", "Files in docs/ not used by the page: " + ", ".join(unused))

    for p in files:
        if p.suffix.lower() in IMAGE_EXT and p.stat().st_size > LARGE_IMAGE_BYTES:
            add("improve", f"Large image {p.name} ({p.stat().st_size / 1024 / 1024:.1f} MB); compress it")

    if git_out(site, "status", "--porcelain", "--", "docs"):
        add("info", "docs/ has uncommitted changes")

    return todos


def site_info(site, manual):
    docs = docs_dir(site)
    logo = next((n for n in ("icon.svg", "logo.png", "logo.svg") if (docs / n).exists()), None)
    mine = manual.get(site["id"], [])
    todos = auto_todos(site) + mine
    detailed = any(re.search(r"screenshot|photo|before/after", t["text"], re.I) for t in mine)
    if detailed:
        todos = [t for t in todos if t["text"] != NO_SCREENSHOT]
    order = {"missing": 0, "improve": 1, "info": 2}
    todos.sort(key=lambda t: order[t["level"]])
    return {
        **site,
        "logo": logo,
        "exists": (docs / "index.html").exists(),
        "branch": git_out(site, "branch", "--show-current"),
        "todos": todos,
    }


def rewrite_html(data):
    text = data.decode("utf-8")
    text = text.replace(CENTRAL_BASE, LOCAL_BASE)
    text = UMAMI_TAG.sub("", text)
    return text.encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("%s\n" % (fmt % args))

    def send_bytes(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, root, rel, rewrite=False):
        root = root.resolve()
        path = (root / rel).resolve()
        inside = path == root or root in path.parents
        if path.is_dir():
            path = path / "index.html"
        if not inside or not path.is_file():
            return self.send_bytes(404, b"Not found", "text/plain; charset=utf-8")
        body = path.read_bytes()
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if rewrite and path.suffix == ".html":
            body = rewrite_html(body)
        if ctype.startswith("text/") or ctype in ("application/javascript", "image/svg+xml"):
            ctype += "; charset=utf-8"
        self.send_bytes(200, body, ctype)

    def do_GET(self):
        url = urlparse(self.path)
        path = unquote(url.path)
        sites = {s["id"]: s for s in load_json("sites.json")}

        if path == "/":
            return self.send_file(HERE, "index.html")
        if path == "/api/sites":
            manual = load_json("todos.json")
            data = {
                "sites": [site_info(s, manual) for s in sites.values()],
                "all": manual.get("_all", []),
            }
            return self.send_bytes(200, json.dumps(data).encode(), "application/json")
        if path.startswith("/dd/"):
            return self.send_file(REPO / "docs", path[len("/dd/"):])
        if path.startswith("/site/"):
            sid, _, rel = path[len("/site/"):].partition("/")
            site = sites.get(sid)
            if not site:
                return self.send_bytes(404, b"Unknown site", "text/plain; charset=utf-8")
            return self.send_file(docs_dir(site), rel, rewrite=True)
        self.send_bytes(404, b"Not found", "text/plain; charset=utf-8")


def bind():
    """Binds the first free port at or above START_PORT."""
    for port in range(START_PORT, START_PORT + MAX_PORT_TRIES):
        try:
            return ThreadingHTTPServer((HOST, port), Handler)
        except OSError:
            print(f"Port {port} is in use, trying {port + 1}")
    sys.exit(f"No free port in {START_PORT}-{START_PORT + MAX_PORT_TRIES - 1}")


def open_browser(url):
    opener = shutil.which("xdg-open")
    if os.environ.get("NO_OPEN") or not opener:
        return
    subprocess.Popen([opener, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    server = bind()
    url = f"http://{HOST}:{server.server_address[1]}/"
    print(f"Preview: {url}  (Ctrl+C to stop)")
    open_browser(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
