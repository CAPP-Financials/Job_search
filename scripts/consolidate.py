"""Merge per-tier agent output (data/raw/*.jsonl) into data/jobs.jsonl, trackers/tracker_<date>.xlsx and digests/<date>.md.
Applies: dedupe, 7-day window, band tagging, fit vs both base resumes. Preserves status/notes edited in the xlsx.
Usage: python scripts/consolidate.py [--days 7] [--today YYYY-MM-DD]
"""
import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from enrich import enrich_row, load_manual, load_profile, write_queue  # noqa: E402

TIERS = ["1", "2", "3A", "3B", "3C"]
TIER_NAME = {"1": "Tier 1 MBB", "2": "Tier 2 Big Four", "3A": "Tier 3A Global strategy",
             "3B": "Tier 3B Transformation+ESG", "3C": "Tier 3C Boutiques+regional"}
BANDS_KEEP = {"Analyst", "Senior Analyst", "Associate", "Senior Associate", "Associate Consultant", "Consultant", "Senior Consultant"}
# Back-end ATS the user reports; everything else stays "unverified" until evidenced.
BACKEND_ATS = {"BCG": "Eightfold (user-reported; Phenom front end seen)",
               "Accenture": "Eightfold (user-reported; Workday apply seen)",
               "McKinsey & Company": "Avature (seen: mckinsey.avature.net)",
               "Bain & Company": "Avature (seen: careers.bain.com, avacdn.net)",
               "Deloitte (global portal)": "Avature (seen on Deloitte portals)",
               "Deloitte USI (India)": "Avature (seen: usijobs.deloitte.com)",
               "Deloitte UK": "Avature (seen: deloitteuk.avature.net)",
               "Deloitte Middle East": "Avature (seen: middleeastjobs.deloitte.com)",
               "PwC India": "Workday (seen: pwc.wd3.myworkdayjobs.com)",
               "PwC global": "Workday (seen: pwc.wd3.myworkdayjobs.com)",
               "PwC UK": "Workday + Phenom front end (seen: jobs.pwc.co.uk)",
               "PwC Middle East": "Workday (seen)",
               "Strategy& (PwC)": "Workday (PwC tenant)",
               "EY careers (global)": "SAP SuccessFactors (seen)",
               "EY-Parthenon": "SAP SuccessFactors (seen)",
               "KPMG India": "Oracle HCM (seen)",
               "KPMG UK": "SAP SuccessFactors (seen)"}

COLS = ["tier", "firm", "title", "band", "gate_verdict", "gate_reasons", "track", "location", "country", "date_status",
        "posted_date", "posted_date_source", "deadline", "deadline_source", "days_old", "fit_A", "fit_B", "best_track",
        "backend_ats", "apply_vendor", "req_id", "years_exp", "years_min", "years_split", "degree_required",
        "degree_preferred", "pedigree_terms", "work_auth_stated", "visa_note", "early_careers_role", "gate_visa", "gate_years", "gate_consulting_exp",
        "gate_degree", "gate_pedigree", "gate_cert", "gate_language", "gate_early_careers",
        "qualifications_required", "qualifications_preferred", "education", "keywords",
        "salary_posted", "salary_source", "summary", "sponsorship_flag", "url", "prior_history", "status", "notes", "enrichment_gaps"]
GAP_FIELDS = ["deadline", "salary_posted", "qualifications_required", "years_exp", "posted_date"]
VERDICT_RANK = {"CLEAR": 0, "RISK": 1, "BLOCKED": 2}

# Weighted JD terms per track: (regex, weight). Fit = weight of JD terms the resume also covers / weight of JD terms.
LEX = {
    "A": [(r"digital strateg", 3), (r"digital transformation", 3), (r"ai[- ]enabled|ai transformation|ai strateg", 3),
          (r"gen(erative)? ?ai|llm", 3), (r"roadmap", 3), (r"business case", 3), (r"operating model", 3),
          (r"data strateg|data[- ]driven|analytics", 2), (r"customer journey", 2), (r"benchmark", 2),
          (r"stakeholder", 2), (r"workshop", 2), (r"hypothes", 2), (r"prioriti[sz]", 2), (r"automation", 2),
          (r"market (entry|sizing|research)", 2), (r"value realization|value realisation|value creation", 2),
          (r"crm|loyalty|cx\b", 1), (r"power bi|tableau|sql|python|excel", 1), (r"powerpoint|storyline|executive", 1),
          (r"change management", 2), (r"technology strateg", 3), (r"cloud", 1)],
    "B": [(r"sustainab", 3), (r"\besg\b", 3), (r"climate", 3), (r"decarboni[sz]|net[- ]zero|carbon", 3),
          (r"csrd|brsr|tcfd|issb|gri\b|sasb|taxonomy", 3), (r"emissions|scope [123]", 2),
          (r"supply chain", 1), (r"stakeholder", 2), (r"report(ing)?", 1), (r"roadmap|strategy", 2),
          (r"due diligence", 1), (r"circular", 2), (r"impact", 1), (r"regulat|complian", 1),
          (r"workshop", 1), (r"benchmark", 2), (r"data|analytics", 1), (r"business case", 2)],
}


def resume_text(p):
    return p.read_text(encoding="utf-8").lower() if p.exists() else ""


def fit(jd, resume, track):
    jd = jd.lower()
    tot = got = 0
    matched, missing = [], []
    for rx, w in LEX[track]:
        if re.search(rx, jd):
            tot += w
            if re.search(rx, resume):
                got += w
                matched.append(rx.split("|")[0].replace("\\b", ""))
            else:
                missing.append(rx.split("|")[0].replace("\\b", ""))
    return (round(100 * got / tot) if tot else None), matched, missing


def parse_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(str(s)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def jid(r):
    key = (r.get("url") or "") or f"{r.get('firm')}|{r.get('req_id')}|{r.get('title')}|{r.get('location')}"
    return hashlib.sha1(key.encode()).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--today", default=str(date.today()))
    a = ap.parse_args()
    today = parse_date(a.today)
    cutoff = today - timedelta(days=a.days)

    prof, manual = load_profile(), load_manual()
    firms = yaml.safe_load((ROOT / "firms" / "firms.yaml").read_text(encoding="utf-8"))["firms"]
    probe = {r["name"]: r for r in json.loads((ROOT / "firms" / "firecrawl_probe.json").read_text(encoding="utf-8"))} \
        if (ROOT / "firms" / "firecrawl_probe.json").exists() else {}
    resA = resume_text(ROOT / "resumes" / "Purushottam_Kumar_Digital_Strategy_AI_Transformation_Resume.md")
    resB = resume_text(ROOT / "resumes" / "Purushottam_Kumar_ESG_Sustainability_Resume.md")

    prior = {}
    (ROOT / "trackers").mkdir(exist_ok=True)
    xl = ROOT / "trackers" / f"tracker_{today}.xlsx"  # one dated tracker per run
    earlier = sorted((ROOT / "trackers").glob("tracker_*.xlsx"))  # status/notes carry over from the latest earlier tracker
    if earlier:
        wb = load_workbook(earlier[-1])
        if "All" in wb.sheetnames:
            ws = wb["All"]
            hdr = [c.value for c in ws[1]]
            for row in ws.iter_rows(min_row=2, values_only=True):
                d = dict(zip(hdr, row))
                if d.get("id"):
                    prior[d["id"]] = {"status": d.get("status"), "notes": d.get("notes")}

    rows, seen = [], set()
    for f in sorted((ROOT / "data" / "raw").glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            r["id"] = jid(r)
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            rows.append(r)

    out, dropped = [], Counter()
    for r in rows:
        pd = parse_date(r.get("posted_date"))
        r["posted_date"] = str(pd) if pd else ""
        if pd and pd < cutoff:
            dropped["older_than_window"] += 1
            continue
        if r.get("band") not in BANDS_KEEP:
            dropped["band_" + str(r.get("band"))] += 1
            continue
        r["days_old"] = (today - pd).days if pd else ""
        jd = " ".join(str(r.get(k) or "") for k in ("title", "summary", "qualifications_required", "qualifications_preferred", "jd_text"))
        r["fit_A"], mA, xA = fit(jd, resA, "A")
        r["fit_B"], mB, xB = fit(jd, resB, "B")
        sa, sb = r["fit_A"] or 0, r["fit_B"] or 0
        r["best_track"] = "A" if sa >= sb else "B"
        r["fit_matched"], r["fit_missing"] = (mA, xA) if sa >= sb else (mB, xB)
        r["backend_ats"] = BACKEND_ATS.get(r["firm"], "unverified")
        p = probe.get(r["firm"], {})
        v = list((p.get("apply_vendor_links") or {}).keys()) or list((p.get("listing_html_markers") or {}).keys())
        r["apply_vendor"] = r.get("apply_vendor") or (v[0] if v else "")
        enrich_row(r, prof, manual)  # hard gates, parsed deadline/salary, manual overrides
        r["enrichment_gaps"] = ", ".join(k for k in GAP_FIELDS if not r.get(k))
        r["keywords"] = ", ".join(r["keywords"]) if isinstance(r.get("keywords"), list) else (r.get("keywords") or "")
        r.update(prior.get(r["id"], {"status": "new", "notes": ""}))
        out.append(r)

    for r in out:  # dated in-window roles first; undated evergreen reqs are real but not "this week"
        r["date_status"] = "in-window" if r["posted_date"] else "undated"
    # gates first: a role that cannot clear screening should never outrank one that can, whatever its keyword fit
    out.sort(key=lambda r: (TIERS.index(str(r["tier"])), VERDICT_RANK[r["gate_verdict"]], r["date_status"] == "undated",
                            -(max(r["fit_A"] or 0, r["fit_B"] or 0))))
    qpath, qn = write_queue(out)
    (ROOT / "data" / "jobs.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out), encoding="utf-8")

    wb = Workbook()
    wb.remove(wb.active)
    head_fill = PatternFill("solid", fgColor="1F3864")

    def sheet(name, data, cols):
        ws = wb.create_sheet(name[:31])
        ws.append(cols)
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = head_fill
        for r in data:
            ws.append([("; ".join(v) if isinstance(v, list) else v) for v in (r.get(c, "") for c in cols)])
        ws.freeze_panes = "D2"
        ws.auto_filter.ref = ws.dimensions
        for i, c in enumerate(cols, 1):
            ws.column_dimensions[get_column_letter(i)].width = 55 if c in ("summary", "qualifications_required", "qualifications_preferred", "url") else (28 if c in ("title", "firm", "keywords", "location") else 14)
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        return ws

    tracker_cols = ["id"] + COLS
    for t in TIERS:
        sheet(TIER_NAME[t], [r for r in out if str(r["tier"]) == t], tracker_cols)
    sheet("All", out, tracker_cols)
    sheet("Actionable", [r for r in out if r["gate_verdict"] != "BLOCKED"], tracker_cols)

    # Gate summary: where the screening wall actually is, by tier and by reason
    gs = []
    for t in TIERS:
        c = Counter(r["gate_verdict"] for r in out if str(r["tier"]) == t)
        gs.append({"view": TIER_NAME[t], "roles": sum(c.values()), "CLEAR": c["CLEAR"], "RISK": c["RISK"], "BLOCKED": c["BLOCKED"]})
    reasons = Counter()
    for r in out:
        for gname in ("visa", "years", "consulting_exp", "degree", "pedigree", "cert", "language", "early_careers"):
            lvl = r.get("gate_" + gname)
            if lvl in ("RISK", "BLOCKED"):
                reasons[(gname, lvl)] += 1
    for (gname, lvl), n in sorted(reasons.items(), key=lambda kv: -kv[1]):
        gs.append({"view": f"gate: {gname}", "roles": n, "CLEAR": "", "RISK": n if lvl == "RISK" else "", "BLOCKED": n if lvl == "BLOCKED" else ""})
    sheet("Gate summary", gs, ["view", "roles", "CLEAR", "RISK", "BLOCKED"])

    # Coverage sheet: every firm, including zero-role firms (low yield never drops a firm)
    cnt = Counter(r["firm"] for r in out)
    cov = []
    for f in firms:
        p = probe.get(f["name"], {})
        cov.append({"tier": str(f["tier"]), "firm": f["name"], "roles_found": cnt.get(f["name"], 0),
                    "tracks": f["tracks"], "regions": ", ".join(f["regions"]),
                    "backend_ats": BACKEND_ATS.get(f["name"], "unverified"),
                    "apply_vendor": ", ".join((p.get("apply_vendor_links") or {}).keys()) or ", ".join((p.get("listing_html_markers") or {}).keys()),
                    "careers_url": f["careers_url"]})
    sheet("Firms", cov, ["tier", "firm", "roles_found", "tracks", "regions", "backend_ats", "apply_vendor", "careers_url"])
    wb.save(xl)

    # digest
    L = [f"# Job search digest {today}", "", f"Window: posted {cutoff} to {today} ({a.days} days). Source: firm career portals.",
         f"Roles kept: {len(out)} | dropped: " + (", ".join(f"{k}={v}" for k, v in dropped.items()) or "none"), ""]
    by_t = defaultdict(list)
    for r in out:
        by_t[str(r["tier"])].append(r)
    vc = Counter(r["gate_verdict"] for r in out)
    L += [f"Gate verdicts: CLEAR {vc['CLEAR']} | RISK {vc['RISK']} | BLOCKED {vc['BLOCKED']}. "
          "BLOCKED roles are counted per tier below, not listed; full detail is in trackers/tracker_<date>.xlsx.", ""]
    for t in TIERS:
        rows_t = by_t[t]
        tv = Counter(r["gate_verdict"] for r in rows_t)
        L += [f"## {TIER_NAME[t]} ({len(rows_t)}: {tv['CLEAR']} clear, {tv['RISK']} risk, {tv['BLOCKED']} blocked)", ""]
        for r in rows_t:
            if r["gate_verdict"] == "BLOCKED":
                continue
            L.append(f"- **{r['gate_verdict']}** | **{r['firm']}** | {r['title']} | {r['band']} | {r['location']} | "
                     f"posted {r['posted_date'] or 'date n/a'} | fit A {r['fit_A']} / B {r['fit_B']} | "
                     f"{r['gate_reasons'] or 'no gate issues'} | [apply]({r['url']})")
        if not rows_t:
            L.append("- none found this window")
        L.append("")
    (ROOT / "digests" / f"{today}.md").write_text("\n".join(L), encoding="utf-8")
    print(f"kept {len(out)}, dropped {dict(dropped)}; per tier " + str({t: len(by_t[t]) for t in TIERS}))


if __name__ == "__main__":
    main()

