"""Cross-process throttled Firecrawl wrapper. Several agents share one per-minute request cap, so every
call goes through here: it takes a lock, enforces a minimum gap between calls, and retries on rate limit.

CLI:    python scripts/fc.py scrape <url> [--wait 5000] [--format markdown|links|rawHtml|"links,markdown"]
        python scripts/fc.py search "<query>" [--limit 5]
Import: from fc import scrape, search      (both return the CLI's stdout text)
"""
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

LOCK = Path(os.environ.get("TEMP", ".")) / "jobsearch_fc.lock"
STAMP = Path(os.environ.get("TEMP", ".")) / "jobsearch_fc.stamp"
GAP = 7.0  # seconds between calls across all processes
FC = shutil.which("firecrawl") or shutil.which("firecrawl.cmd")


def _acquire(timeout=600):
    t0 = time.time()
    while True:
        try:
            os.mkdir(LOCK)  # atomic on NTFS
            return
        except FileExistsError:
            if time.time() - t0 > timeout:
                try:
                    os.rmdir(LOCK)  # stale lock
                except OSError:
                    pass
            time.sleep(0.3)


def _release():
    try:
        os.rmdir(LOCK)
    except OSError:
        pass


def _call(args, timeout=150):
    for attempt in range(5):
        _acquire()
        try:
            last = float(STAMP.read_text()) if STAMP.exists() else 0.0
            wait = GAP - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
            p = subprocess.run([FC, *args], capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
            STAMP.write_text(str(time.time()))
        finally:
            _release()
        out = (p.stdout or "") + (p.stderr or "")
        if p.returncode == 0:
            return p.stdout
        if "rate limit" in out.lower():
            time.sleep(30)
            continue
        raise RuntimeError(out.strip()[:300])
    raise RuntimeError("rate-limited after retries")


def scrape(url, fmt="markdown", wait=3000):
    return _call(["scrape", url, "-f", fmt, "--wait-for", str(wait)] + (["--json"] if "," in fmt else []))


def search(query, limit=5):
    return _call(["search", query, "--limit", str(limit), "--json"], timeout=90)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("scrape", "search"):
        sys.exit(__doc__)
    if a[0] == "scrape":
        fmt = a[a.index("--format") + 1] if "--format" in a else "markdown"
        wait = int(a[a.index("--wait") + 1]) if "--wait" in a else 3000
        sys.stdout.write(scrape(a[1], fmt, wait))
    else:
        lim = int(a[a.index("--limit") + 1]) if "--limit" in a else 5
        sys.stdout.write(search(a[1], lim))
