"""Render each firm's careers page with Firecrawl and work out two things:
  1. the listing platform (what serves the search page)
  2. the apply platform (where job/apply links actually go) -- this is the ATS the resume has to pass
Failed/404 URLs get a Firecrawl search fallback that proposes replacement URLs.
Writes firms/firecrawl_probe.json. Raw scrapes are cached in .firecrawl_cache/ (gitignored).

Usage: python scripts/firecrawl_pass.py [--only "BCG,Accenture"] [--refresh]
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".firecrawl_cache"
FC = shutil.which("firecrawl") or shutil.which("firecrawl.cmd")

# vendor -> regex tested against LINK urls (apply side) and against HTML (listing side).
# Link patterns are deliberately specific: host or a vendor-only path shape.
LINK_SIGS = {
    "eightfold": r"eightfold\.ai|/careerhub/explore/jobs|/careers\?pid=|[?&]pid=\d{9,}",
    "workday": r"myworkdayjobs\.com|\.myworkdaysite\.com|wd\d+\.myworkday",
    "successfactors": r"successfactors\.(com|eu)|jobs2web\.com|career\d*\.sapsf\.|/talentcommunity/|/job/[^/]+/\d+-?/?$",
    "oracle-hcm": r"oraclecloud\.com/hcmUI|/hcmUI/CandidateExperience|candidateexperience",
    "taleo": r"taleo\.net",
    "icims": r"icims\.com",
    "avature": r"avature\.net",
    "greenhouse": r"greenhouse\.io",
    "lever": r"jobs\.lever\.co",
    "smartrecruiters": r"smartrecruiters\.com",
    "jobvite": r"jobvite\.com",
    "brassring": r"brassring\.com",
    "ashby": r"ashbyhq\.com",
    "workable": r"workable\.com",
    "recruitee": r"recruitee\.com",
    "teamtailor": r"teamtailor\.com",
    "personio": r"personio\.(de|com)",
    "darwinbox": r"darwinbox\.(in|com)",
    "zoho-recruit": r"zohorecruit|zoho\.com/recruit",
    "bamboohr": r"bamboohr\.com",
    "jazzhr": r"applytojob\.com|jazz\.co",
    "cornerstone": r"csod\.com",
    "dayforce": r"dayforcehcm\.com|ceridian",
    "pageup": r"pageuppeople\.com|pageup\.com",
    "beamery": r"beamery\.com",
}
HTML_SIGS = {  # listing-layer markers, matched on rendered HTML
    "phenom": r"phenompeople|ph-cdn|phenom\.com|phApp|utm_source=Phenom",
    "eightfold": r"eightfold\.ai|eightfold",
    "workday": r"myworkdayjobs\.com|wd\d+\.myworkdayjobs",
    "successfactors": r"successfactors|jobs2web",
    "oracle-hcm": r"oraclecloud\.com/hcmUI|CandidateExperience",
    "avature": r"avature\.net",
    "icims": r"icims\.com",
    "taleo": r"taleo\.net",
    "greenhouse": r"greenhouse\.io|boards\.greenhouse",
    "smartrecruiters": r"smartrecruiters\.com",
    "darwinbox": r"darwinbox",
    "zoho-recruit": r"zohorecruit|zoho\.com/recruit",
    "wordpress-wp-job-manager": r"wp-job-manager|job_listing",
}
JOBISH = re.compile(r"job|career|vacanc|opening|position|requisition|apply|talent|recruit|opportunit", re.I)


def run(cmd, timeout=150):
    p = subprocess.run([FC, *cmd], capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def scrape(url, name, refresh):
    out = CACHE / (slug(name) + ".json")
    if out.exists() and not refresh:
        return json.loads(out.read_text(encoding="utf-8")), None
    for attempt in range(4):  # per-minute rate limit: back off and retry, never record it as a firm failure
        time.sleep(7)
        rc, msg = run(["scrape", url, "-f", "links,rawHtml", "--wait-for", "5000", "--json", "-o", str(out)])
        if rc == 0 and out.exists():
            break
        if "rate limit" not in msg.lower():
            return None, msg.strip()[:200]
        time.sleep(35)
    else:
        return None, "rate-limited after retries"
    if rc != 0 or not out.exists():
        return None, msg.strip()[:200]
    try:
        d = json.loads(out.read_text(encoding="utf-8"))
        return d.get("data", d), None
    except Exception as e:
        return None, f"bad json: {e}"


def analyse(d):
    links = [l.replace("&amp;", "&") for l in (d.get("links") or [])]
    html = d.get("rawHtml") or ""
    meta = d.get("metadata") or {}
    link_counts = Counter()
    for l in links:
        for v, rx in LINK_SIGS.items():
            if re.search(rx, l, re.I):
                link_counts[v] += 1
    html_counts = Counter()
    for v, rx in HTML_SIGS.items():
        n = len(re.findall(rx, html, re.I))
        if n:
            html_counts[v] = n
    hosts = Counter(urlparse(l).netloc for l in links if JOBISH.search(l))
    page_host = urlparse(meta.get("sourceURL") or meta.get("url") or "").netloc
    ext_hosts = {h: n for h, n in hosts.most_common(8) if h and h != page_host}
    jobs = [l for l in links if re.search(r"/job[s]?/|jobdetail|/careerhub/|requisition|/position", l, re.I)]
    return {
        "status_code": meta.get("statusCode"),
        "final_url": meta.get("sourceURL") or meta.get("url"),
        "n_links": len(links),
        "html_bytes": len(html),
        "apply_vendor_links": dict(link_counts.most_common(4)),
        "listing_html_markers": dict(html_counts.most_common(4)),
        "external_job_hosts": ext_hosts,
        "sample_job_links": jobs[:3],
    }


def find_alternatives(name):
    rc, msg = run(["search", f"{name} careers jobs apply", "--limit", "4", "--json"], timeout=90)
    try:
        j = json.loads(msg[msg.index("{"):]) if "{" in msg else {}
    except Exception:
        return []
    res = (j.get("data") or j).get("web") if isinstance(j.get("data") or j, dict) else None
    res = res or j.get("results") or []
    return [r.get("url") for r in res if isinstance(r, dict) and r.get("url")][:4]


def one(args):
    f, refresh = args
    r = {"name": f["name"], "tier": str(f["tier"]), "url": f["careers_url"]}
    d, err = scrape(f["careers_url"], f["name"], refresh)
    if d is None:
        r["error"] = err
        if "rate-limited" not in (err or ""):
            r["alternatives"] = find_alternatives(f["name"])
        return r
    r.update(analyse(d))
    code = r.get("status_code")
    if (code and code >= 400) or r["n_links"] < 3:
        time.sleep(7)
        r["alternatives"] = find_alternatives(f["name"])
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    if not FC:
        sys.exit("firecrawl CLI not on PATH")
    CACHE.mkdir(exist_ok=True)
    firms = yaml.safe_load((ROOT / "firms" / "firms.yaml").read_text(encoding="utf-8"))["firms"]
    if a.only:
        want = {x.strip().lower() for x in a.only.split(",")}
        firms = [f for f in firms if any(w in f["name"].lower() for w in want)]
    with ThreadPoolExecutor(1) as ex:  # sequential: the per-minute request cap is the binding limit, not concurrency
        res = list(ex.map(one, [(f, a.refresh) for f in firms]))
    out = ROOT / "firms" / "firecrawl_probe.json"
    prev = {}
    if out.exists() and a.only:
        prev = {r["name"]: r for r in json.loads(out.read_text(encoding="utf-8"))}
    prev.update({r["name"]: r for r in res})
    out.write_text(json.dumps(list(prev.values()), indent=1), encoding="utf-8")
    for r in res:
        v = r.get("apply_vendor_links") or {}
        h = r.get("listing_html_markers") or {}
        print(f"{r['tier']:>2} {r['name'][:30]:30} http={r.get('status_code')} links={r.get('n_links')} "
              f"apply={list(v)[:2]} listing={list(h)[:2]} ext={list(r.get('external_job_hosts', {}))[:2]} "
              f"{'ERR ' + r['error'][:60] if r.get('error') else ''}{' ALT ' + str(r.get('alternatives', [])[:1]) if r.get('alternatives') else ''}")


if __name__ == "__main__":
    main()
