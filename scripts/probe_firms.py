"""One request per firm: does the careers URL resolve, and which ATS family is behind it?
Writes firms/probe.json and firms/FIRMS.md (tiered, readable). Does not touch firms.yaml.
Usage: python scripts/probe_firms.py
"""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
       "Accept-Language": "en"}

# (ats label, regex on final URL + html). First match wins; order is most specific first.
SIGS = [
    ("workday", r"myworkdayjobs\.com|wd\d+\.myworkday"),
    ("eightfold", r"eightfold\.ai|\.eightfold\."),
    ("successfactors", r"successfactors|jobs2web|career\d*\.sap\.com|\.sapsf\."),
    ("phenom", r"phenom(people)?\.com|ph-cdn|phenompeople"),
    ("icims", r"icims\.com"),
    ("taleo", r"taleo\.net"),
    ("greenhouse", r"greenhouse\.io|boards\.greenhouse"),
    ("lever", r"jobs\.lever\.co"),
    ("smartrecruiters", r"smartrecruiters\.com"),
    ("oracle-hcm", r"oraclecloud\.com/hcmUI|candidateexperience"),
    ("avature", r"avature\.net"),
    ("jobvite", r"jobvite\.com"),
    ("brassring", r"brassring\.com"),
    ("zohorecruit", r"zohorecruit|zoho\.com/recruit"),
    ("workable", r"workable\.com"),
    ("recruitee", r"recruitee\.com"),
    ("breezy", r"breezy\.hr"),
    ("darwinbox", r"darwinbox\.in|darwinbox\.com"),
    ("keka", r"keka(hr)?\.com"),
]


def probe(f):
    out = {"name": f["name"], "tier": f["tier"], "url": f["careers_url"]}
    try:
        r = requests.get(f["careers_url"], headers=UA, timeout=20, allow_redirects=True)
        hay = r.url + "\n" + r.text[:400_000]
        ats = next((a for a, rx in SIGS if re.search(rx, hay, re.I)), None)
        blocked = r.status_code in (401, 403, 429) or bool(re.search(r"just a moment|cf-chl|captcha|access denied", r.text[:3000], re.I))
        out.update(status=r.status_code, final_url=r.url, bytes=len(r.text), ats=ats or "unknown",
                   blocked=blocked, js_shell=len(r.text) < 4000)
    except Exception as e:  # report per firm, never stop the run
        out.update(status=None, final_url=None, ats="unreachable", error=type(e).__name__ + ": " + str(e)[:120])
    return out


def verdict(p):
    if p["ats"] == "unreachable":
        return "UNREACHABLE, check URL"
    if p.get("blocked"):
        return "bot-blocked, needs Firecrawl/browser"
    if p["status"] and p["status"] >= 400:
        return f"HTTP {p['status']}, check URL"
    if p["ats"] != "unknown":
        return "ok"
    return "ok, ATS not detected (JS shell?)" if p.get("js_shell") else "ok, ATS not detected"


def main():
    firms = yaml.safe_load((ROOT / "firms" / "firms.yaml").read_text(encoding="utf-8"))["firms"]
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(probe, firms))
    by_name = {r["name"]: r for r in res}
    (ROOT / "firms" / "probe.json").write_text(json.dumps(res, indent=1), encoding="utf-8")

    order = ["1", "2", "3A", "3B", "3C"]
    titles = {"1": "Tier 1: MBB", "2": "Tier 2: Big Four", "3A": "Tier 3A: Global strategy firms",
              "3B": "Tier 3B: Transformation, tech and specialist (incl. ESG)", "3C": "Tier 3C: Boutiques and regional"}
    lines = ["# Firm registry (draft for review)", "",
             "Source: `firms/firms.yaml`. ATS and status come from one live request per firm (`firms/probe.json`).",
             "Tracks: A = Digital Strategy & AI, B = Sustainability/ESG.", ""]
    for t in order:
        rows = [f for f in firms if str(f["tier"]) == t]
        lines += [f"## {titles[t]} ({len(rows)})", ""]
        for f in rows:
            p = by_name[f["name"]]
            lines.append(f"- **{f['name']}** | tracks {f['tracks']} | {', '.join(f['regions'])} | ATS: {p['ats']} | {verdict(p)}")
            lines.append(f"  - {f['careers_url']}" + (f"  (landed on {p['final_url']})" if p.get('final_url') and p['final_url'].rstrip('/') != f['careers_url'].rstrip('/') else ""))
            if f.get("notes"):
                lines.append(f"  - note: {f['notes']}")
        lines.append("")
    ok = sum(1 for r in res if verdict(r) == "ok")
    lines += ["## Probe summary", "", f"- {len(res)} firms, {ok} clean, "
              f"{sum(1 for r in res if r.get('blocked'))} bot-blocked, "
              f"{sum(1 for r in res if r['ats'] == 'unreachable' or (r['status'] or 0) >= 400)} need URL fixes, "
              f"{sum(1 for r in res if r['ats'] == 'unknown')} with no ATS detected."]
    (ROOT / "firms" / "FIRMS.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[-3:]))
    for r in res:
        print(f"{r['tier']:>2} {r['name'][:34]:34} {str(r['status']):>4} {r['ats']:15} {verdict(r)}")


if __name__ == "__main__":
    sys.exit(main())
