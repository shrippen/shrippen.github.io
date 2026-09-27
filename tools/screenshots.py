#!/usr/bin/env python3
"""Takes the landing-page screenshots of every project from its demo data.

Usage: tools/.venv/bin/python tools/screenshots.py [id ...] [--lang de,en] [--theme T]
                                                   [--list] [--dry-run] [--keep-running]
Setup once: python3 -m venv tools/.venv && tools/.venv/bin/pip install playwright pillow
(Chromium comes from /usr/bin/chromium, no Playwright browser download.)

Every project describes its shots in <project>/demo/shots.json (ids and folders
from preview/sites.json plus EXTRA below). Images land in
<project>/docs/shots/<name>-<lang>[-<theme>].<format>.

shots.json:
  kind       "web": start the demo, then Playwright visits the shots.
             "command": the start command writes <name>.png files to $SHOT_DIR itself
             (Plasma widgets, PaperTTY, native windows).
  start      shell command, run in the project folder. Placeholders {lang} {theme} {port} {root}.
             Env: DEMO_TODAY, DEMO_LANG, DEMO_THEME, SHOT_DIR, SHOT_PLAN (the shots as JSON), PORT.
  detach     true if start returns after the demo runs in the background (docker).
  stop       optional shell command after the shots (with detach).
  ready      URL that must answer 200 before the shots ({port}); or
  ready_line regex on the start command's output; group 1 (if any) becomes {base}.
  base       base URL for relative shot URLs ({port}).
  group      projects with the same group share one start per lang/theme (the Kimai plugins).
  langs      default ["de", "en"];  themes: default [""] (no suffix)
  today      DEMO_TODAY for this project, default demo/world.json screenshot_today
  viewport   [w, h], scale (device pixel ratio, default 2), format (webp|png|jpg, default webp)
  setup      actions once per start (login), each shot: {name, url, wait, clip, full_page,
             viewport, actions, manual}. Actions: {"fill": sel, "value": v}, {"click": sel},
             {"dblclick": sel}, {"press": key}, {"wait": sel}, {"sleep": ms}, {"goto": url}, {"eval": js}.
             Strings in actions may use {lang}, {base}, {user}, {password}.
  manual     a shot that is still taken by hand: listed in the summary, never taken.
"""
import json
import os
import re
import shlex
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO.parent
WORLD = json.loads((REPO / "demo" / "world.json").read_text(encoding="utf-8"))
CHROMIUM = os.environ.get("CHROMIUM", "/usr/bin/chromium")
READY_TIMEOUT = 300
# Projects with a demo that are not on the overview page (preview/sites.json).
EXTRA = [
    {"id": "andon", "dir": "andon"},
    {"id": "kimai-farbfaecher", "dir": "Kimai Farbfächer"},
]


def sites():
    listed = json.loads((REPO / "preview" / "sites.json").read_text(encoding="utf-8"))
    return [s for s in listed if s["id"] != "overview"] + EXTRA


def load_manifests(ids):
    out = []
    for site in sites():
        if ids and site["id"] not in ids:
            continue
        folder = ROOT / site["dir"]
        path = folder / "demo" / "shots.json"
        if not path.exists():
            out.append((site, folder, None))
            continue
        out.append((site, folder, json.loads(path.read_text(encoding="utf-8"))))
    return out


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def fmt(value, ctx):
    """Fills {name} placeholders from ctx; other braces (JS, shell) stay as they are."""
    if isinstance(value, str):
        return re.sub(r"\{(\w+)\}", lambda m: str(ctx[m.group(1)]) if m.group(1) in ctx else m.group(0), value)
    if isinstance(value, list):
        return [fmt(v, ctx) for v in value]
    if isinstance(value, dict):
        return {k: fmt(v, ctx) for k, v in value.items()}
    return value


class Demo:
    """One running demo (start command) for a project or group."""

    def __init__(self, folder, manifest, ctx, env, log):
        self.folder, self.m, self.ctx, self.env, self.log = folder, manifest, ctx, env, log
        self.proc = None
        self.lines = []

    def start(self):
        cmd = fmt(self.m["start"], self.ctx)
        self.log(f"  $ {cmd}")
        self.proc = subprocess.Popen(cmd, shell=True, cwd=self.folder, env=self.env, text=True,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
        threading.Thread(target=self._pump, daemon=True).start()
        if self.m.get("detach"):
            if self.proc.wait() != 0:
                raise RuntimeError("start failed:\n" + "".join(self.lines[-30:]))
        self._wait_ready()

    def _pump(self):
        for line in self.proc.stdout:
            self.lines.append(line)
            if os.environ.get("SHOTS_VERBOSE"):
                sys.stdout.write("    | " + line)

    def _wait_ready(self):
        deadline = time.time() + self.m.get("timeout", READY_TIMEOUT)
        pattern = self.m.get("ready_line")
        url = fmt(self.m["ready"], self.ctx) if self.m.get("ready") else None
        while time.time() < deadline:
            if pattern:
                for line in self.lines:
                    hit = re.search(pattern, line)
                    if hit:
                        if hit.groups():
                            self.ctx["base"] = hit.group(1).rstrip("/")
                        return
            elif url:
                try:
                    with urllib.request.urlopen(url, timeout=3) as r:
                        if r.status < 500:
                            return
                except Exception:
                    pass
            else:
                return
            if not self.m.get("detach") and self.proc.poll() is not None and self.m["kind"] == "web":
                raise RuntimeError("demo exited early:\n" + "".join(self.lines[-30:]))
            time.sleep(0.5)
        raise RuntimeError("demo not ready in time:\n" + "".join(self.lines[-30:]))

    def wait_command(self):
        timeout = self.m.get("timeout", READY_TIMEOUT)
        try:
            code = self.proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            self.stop()
            raise RuntimeError("command timed out:\n" + "".join(self.lines[-30:]))
        if code != 0:
            raise RuntimeError(f"command exited {code}:\n" + "".join(self.lines[-30:]))

    def stop(self):
        if self.m.get("stop"):
            subprocess.run(fmt(self.m["stop"], self.ctx), shell=True, cwd=self.folder, env=self.env,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if self.proc and self.proc.poll() is None:
            try:
                os.killpg(self.proc.pid, signal.SIGTERM)
                self.proc.wait(timeout=10)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                try:
                    os.killpg(self.proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass


def save_image(png_path, out_path, fmt_name):
    from PIL import Image
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(png_path)
    if fmt_name == "png":
        img.save(out_path, optimize=True)
    elif fmt_name == "jpg":
        img.convert("RGB").save(out_path, quality=88, optimize=True, progressive=True)
    else:
        img.save(out_path, quality=88, method=6)


def out_name(shot, lang, theme, fmt_name):
    suffix = f"-{theme}" if theme else ""
    return f"{shot['name']}-{lang}{suffix}.{fmt_name}"


def run_actions(page, actions, ctx):
    for a in fmt(actions or [], ctx):
        if "fill" in a:
            page.fill(a["fill"], a["value"])
        elif "click" in a:
            page.locator(a["click"]).first.click()
        elif "dblclick" in a:
            page.locator(a["dblclick"]).first.dblclick()
        elif "press" in a:
            page.keyboard.press(a["press"])
        elif "wait" in a:
            page.wait_for_selector(a["wait"], timeout=30000)
        elif "sleep" in a:
            page.wait_for_timeout(a["sleep"])
        elif "goto" in a:
            page.goto(a["goto"] if "://" in a["goto"] else ctx["base"] + a["goto"], wait_until="networkidle")
        elif "eval" in a:
            page.evaluate(a["eval"])
        else:
            raise ValueError(f"unknown action {a}")


def web_shots(browser, jobs, ctx, log):
    """jobs: [(site, folder, manifest)] sharing one running demo."""
    results = []
    first = jobs[0][2]
    vw, vh = first.get("viewport", [1440, 900])
    context = browser.new_context(viewport={"width": vw, "height": vh},
                                  device_scale_factor=first.get("scale", 2),
                                  locale="de-DE" if ctx["lang"] == "de" else "en-GB",
                                  timezone_id=WORLD["timezone"], color_scheme="dark")
    page = context.new_page()
    done_setup = set()
    for site, folder, m in jobs:
        key = json.dumps(m.get("setup", []))
        if key not in done_setup:
            run_actions(page, m.get("setup"), ctx)
            done_setup.add(key)
        for shot in m["shots"]:
            if shot.get("manual"):
                results.append((site["id"], shot["name"], "manual", None))
                continue
            target = folder / "docs" / "shots" / out_name(shot, ctx["lang"], ctx["theme"], m.get("format", "webp"))
            try:
                if shot.get("viewport"):
                    page.set_viewport_size({"width": shot["viewport"][0], "height": shot["viewport"][1]})
                if shot.get("url"):
                    url = fmt(shot["url"], ctx)
                    page.goto(url if "://" in url else ctx["base"] + url, wait_until="networkidle")
                run_actions(page, shot.get("actions"), ctx)
                if shot.get("wait"):
                    page.wait_for_selector(shot["wait"], timeout=30000)
                page.wait_for_timeout(shot.get("settle", 400))
                with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
                    if shot.get("clip"):
                        page.locator(shot["clip"]).first.screenshot(path=tmp.name, animations="disabled")
                    else:
                        page.screenshot(path=tmp.name, full_page=shot.get("full_page", False), animations="disabled")
                    save_image(tmp.name, target, m.get("format", "webp"))
                results.append((site["id"], shot["name"], "ok", target))
                log(f"  ok {target.relative_to(ROOT)}")
            except Exception as e:  # keep going, report at the end
                results.append((site["id"], shot["name"], "failed", str(e).splitlines()[0]))
                log(f"  FAILED {site['id']}/{shot['name']}: {str(e).splitlines()[0]}")
            finally:
                if shot.get("viewport"):
                    page.set_viewport_size({"width": vw, "height": vh})
    context.close()
    return results


def command_shots(site, folder, m, demo, ctx, shot_dir, log):
    demo.wait_command()
    results = []
    for shot in m["shots"]:
        if shot.get("manual"):
            results.append((site["id"], shot["name"], "manual", None))
            continue
        src = Path(shot_dir) / f"{shot['name']}.png"
        target = folder / "docs" / "shots" / out_name(shot, ctx["lang"], ctx["theme"], m.get("format", "webp"))
        if not src.exists():
            results.append((site["id"], shot["name"], "failed", "not written by the start command"))
            log(f"  FAILED {site['id']}/{shot['name']}: not written")
            continue
        save_image(src, target, m.get("format", "webp"))
        results.append((site["id"], shot["name"], "ok", target))
        log(f"  ok {target.relative_to(ROOT)}")
    return results


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--lang", default="")
    ap.add_argument("--theme", default="")
    ap.add_argument("--list", action="store_true", help="show manifests and shots, take nothing")
    ap.add_argument("--dry-run", action="store_true", help="print what would run")
    ap.add_argument("--keep-running", action="store_true", help="do not stop detached demos")
    args = ap.parse_args(argv)
    log = lambda s: print(s, flush=True)

    manifests = load_manifests(set(args.ids))
    missing = [s["id"] for s, _, m in manifests if m is None]
    manifests = [x for x in manifests if x[2] is not None]
    if args.list or args.dry_run:
        for site, folder, m in manifests:
            langs = args.lang.split(",") if args.lang else m.get("langs", ["de", "en"])
            print(f"{site['id']:18} {m['kind']:8} {','.join(langs):6} "
                  + ", ".join(s["name"] + (" (manual)" if s.get("manual") else "") for s in m["shots"]))
        if missing:
            print("no demo/shots.json: " + ", ".join(missing))
        return 0

    # Group runs: (group or id, lang, theme) -> jobs
    runs = {}
    for site, folder, m in manifests:
        langs = args.lang.split(",") if args.lang else m.get("langs", ["de", "en"])
        themes = [args.theme] if args.theme else m.get("themes", [""])
        for lang in langs:
            for theme in themes:
                runs.setdefault((m.get("group") or site["id"], lang, theme), []).append((site, folder, m))

    results = []
    pw = browser = None
    try:
        for (key, lang, theme), jobs in runs.items():
            site, folder, m = jobs[0]
            log(f"== {key} [{lang}{'/' + theme if theme else ''}]")
            port = free_port()
            shot_dir = tempfile.mkdtemp(prefix=f"shots-{site['id']}-")
            ctx = {"lang": lang, "theme": theme, "port": port, "root": str(ROOT), "repo": str(REPO),
                   "user": m.get("user", ""), "password": m.get("password", WORLD["demo_password"])}
            ctx["base"] = fmt(m.get("base", "http://127.0.0.1:{port}"), ctx)
            env = dict(os.environ, DEMO_TODAY=m.get("today", WORLD["screenshot_today"]), DEMO_LANG=lang,
                       DEMO_THEME=theme or "default", SHOT_DIR=shot_dir, PORT=str(port),
                       SHOT_PLAN=json.dumps([s for s in m["shots"] if not s.get("manual")]))
            demo = Demo(folder, m, ctx, env, log)
            try:
                demo.start()
                if m["kind"] == "command":
                    for s, f, mm in jobs:
                        results += command_shots(s, f, mm, demo, ctx, shot_dir, log)
                else:
                    if browser is None:
                        from playwright.sync_api import sync_playwright
                        pw = sync_playwright().start()
                        browser = pw.chromium.launch(executable_path=CHROMIUM, args=["--no-sandbox"])
                    results += web_shots(browser, jobs, ctx, log)
            except Exception as e:
                log(f"  FAILED {key}: {e}")
                for s, _, mm in jobs:
                    results += [(s["id"], sh["name"], "failed", str(e).splitlines()[0]) for sh in mm["shots"]]
            finally:
                if not args.keep_running:
                    demo.stop()
    finally:
        if browser:
            browser.close()
            pw.stop()

    ok = [r for r in results if r[2] == "ok"]
    failed = [r for r in results if r[2] == "failed"]
    manual = sorted({(r[0], r[1]) for r in results if r[2] == "manual"})
    print(f"\n{len(ok)} screenshots, {len(failed)} failed, {len(manual)} manual")
    for pid, name, _, why in failed:
        print(f"  failed  {pid}/{name}: {why}")
    for pid, name in manual:
        print(f"  manual  {pid}/{name}")
    if missing:
        print("  no demo/shots.json: " + ", ".join(missing))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
