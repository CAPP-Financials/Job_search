"""Enrichment: extract HARD gates from each JD and judge them against profile.yaml.
Fit by keywords says how well the resume reads; gates say whether the application can get past
screening at all. Verdict per role: CLEAR | RISK | BLOCKED, with the reasons spelled out.

Module use:  from enrich import load_profile, load_manual, enrich_row
CLI:         python scripts/enrich.py --selftest
"""
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PREF = re.compile(r"(?i)\b(prefer\w*|plus|desirable|advantage|nice to have|bonus|ideally|beneficial|a plus)\b")
MUST = re.compile(r"(?i)\b(required|must|mandatory|essential|need to|necessary|minimum)\b")

CONSULT_NEAR = re.compile(r"(?i)(consult|big ?4|big ?four|mbb|professional services|advisory|strategy firm)")
YEARS_PATTERNS = [
    re.compile(r"(?i)\b(\d{1,2})\s*(?:-|–|to)\s*(\d{1,2})\s*\+?\s*years?"),
    re.compile(r"(?i)\b(\d{1,2})\s*\+\s*years?"),
    re.compile(r"(?i)(?:at least|minimum(?: of)?|min\.?|over|more than|atleast)\s*(\d{1,2})\s*\+?\s*years?"),
    re.compile(r"(?i)\b(\d{1,2})\s*years?(?:['’]s?)?\s+(?:of\s+)?(?:relevant|professional|work|industry|hands-on|prior|post[- ]qualification|post[- ]mba)?\s*(?:experience|exposure|background)"),
]
EXP_CTX = re.compile(r"(?i)(experience|exposure|background|track record|in (?:a )?(?:consult|strategy|analytic|data|sustainab|esg)|working)")
# school pedigree vs prior-employer pedigree are different screens; both are labelled in the output
PED_SCHOOL = re.compile(r"(?i)((?:top[- ]tier|top[- ]ranked|top[- ]\d+|premier|leading|reputable|prestigious|tier[- ]?1|ivy|russell group|oxbridge|target)"
                        r"\W+(?:\w+\W+){0,3}?(?:universit\w+|institut\w+|college|business school|mba)|"
                        r"\b(?:iim|isb)\b|excellent academic|strong academic|top academic|outstanding academic|first[- ]class degree)")
PED_EMPLOYER = re.compile(r"(?i)((?:top[- ]tier|tier[- ]?1|leading|blue[- ]chip|big ?4|big ?four|mbb|top)\W+(?:\w+\W+){0,2}?"
                          r"(?:consult\w+ firm|consultancy|strategy firm|professional services firm))")
LANG_PREF = re.compile(r"(?i)(priorit\w+|an? asset|advantage|welcome|bonus|desirable|preferred|plus)")
DEGREE_LEVELS = [("PhD", r"(?i)\b(ph\.?d|doctorate)\b"),
                 ("Master", r"(?i)\b(master|mba|post[- ]?graduate|pgdm|m\.?sc|m\.?tech)\b"),
                 ("Bachelor", r"(?i)\b(bachelor|undergraduate|b\.?tech|b\.?e\b|b\.?sc|b\.?com)\b")]
CERT = re.compile(r"\b(chartered accountant|C\.A\.|ACCA|CPA|CFA|FRM|PMP|Six Sigma|PRINCE2|CISA|CISSP|CMA|ICAI|FCCA)\b")
CA_BARE = re.compile(r"\bCA\b")  # also "California" / nav footers, so only counted in a qualification sentence
CA_CTX = re.compile(r"(?i)\b(mba|cfa|pgdm|pgdbm|qualif\w*|chartered|degree|icwa|cma|cpa)\b")
LANG = re.compile(r"(?i)\b(german|french|arabic|dutch|spanish|mandarin|japanese|italian|polish|portuguese|swedish|norwegian|danish|finnish|korean)\b"
                  r"(?:[^.\n]{0,40}\b(?:fluen|native|proficien|speak|language|written|spoken)|\s+(?:language|speaker|fluency))"
                  r"|(?:fluent|native|proficien\w+|business[- ]level)\s+(?:in\s+)?(?:german|french|arabic|dutch|spanish|mandarin|japanese|italian|polish|portuguese)")
LANG_NAME = re.compile(r"(?i)\b(german|french|arabic|dutch|spanish|mandarin|japanese|italian|polish|portuguese|swedish|norwegian|danish|finnish|korean)\b")
AUTH_NOT = re.compile(r"(?i)(unable to (?:offer |provide )?(?:visa )?sponsor|cannot (?:offer |provide )?(?:visa )?sponsor|"
                      r"(?:do|does|will) not (?:offer |provide )?(?:visa )?sponsor|no (?:visa )?sponsorship|not (?:able|in a position) to sponsor|"
                      r"without (?:the need for )?sponsorship|sponsorship (?:is )?not (?:available|offered|provided))")
AUTH_RTW = re.compile(r"(?i)(right to work|legally (?:authori[sz]ed|entitled|eligible)|authori[sz]ed to work|eligible to work|work (?:permit|authori[sz]ation)|citizen|permanent resident)")
AUTH_CLEAR = re.compile(r"(?i)(security clearance|sc[- ]cleared|dv[- ]cleared|clearance (?:is )?required)")
AUTH_OFFER = re.compile(r"(?i)((?:visa|relocation)(?: support| sponsorship| assistance)?(?: is| will be)? (?:available|provided|offered|supported)|"
                        r"we (?:will |can )?sponsor|sponsorship (?:is )?(?:available|offered|provided)|relocation (?:assistance|package|support|allowance))")
# Early-careers ROLE (informational): fine to apply to. "early careers"/"campus" also appear in scraped nav, so not used.
GRAD_ROLE = re.compile(r"(?i)(graduate (?:scheme|programme|program|intake|trainee)|graduate analyst|campus (?:hire|hiring))")
# Early-careers ELIGIBILITY that a completed graduate cannot meet: must graduate in the future / be a current student.
GRAD_FUTURE = re.compile(r"(?i)((?:graduat(?:ing|e|ion)|to graduate|will graduate|expected (?:to )?graduat\w*|completing (?:your|their|a)\b[^.\n]{0,25}(?:degree|studies))"
                         r"[^.\n]{0,70}\b(?:20(?:2[6-9]|3\d))\b|class of 20(?:2[6-9]|3\d)|final[- ]year (?:student|undergrad|bachelor|master|mba)|penultimate[- ]year|"
                         r"currently (?:enrolled|studying|pursuing)|current (?:university )?student|"
                         r"(?:must|should|need to) (?:be|have)[^.\n]{0,25}(?:enrolled|student)|graduates? (?:of|from|in)\s+(?:the )?class of)")
DEADLINE = [re.compile(r"(?i)(?:apply|applications?|submit(?:ted)?|submission)\s+(?:by|before|until|no later than|on or before)\s+([^.\n;|]{6,32})"),
            re.compile(r"(?i)(?:closing date|closes?(?: on)?|deadline|last date(?: to apply)?|applications? clos\w+(?: on)?)\s*[:\-–]?\s*([^.\n;|]{6,32})")]
SALARY = re.compile(r"(?i)((?:₹|INR|Rs\.?|USD|US\$|\$|£|GBP|€|EUR|AED|SGD|CAD|AUD)\s?\d[\d,.]*\s?(?:k|lakhs?|lpa|l\b|crores?|cr\b|million|m\b)?"
                    r"(?:\s?(?:-|–|to)\s?(?:₹|INR|Rs\.?|USD|US\$|\$|£|GBP|€|EUR|AED|SGD|CAD|AUD)?\s?\d[\d,.]*\s?(?:k|lakhs?|lpa|l\b|crores?|cr\b|million|m\b)?)?"
                    r"(?:\s?(?:per|/|a)\s?(?:year|annum|yr|month|mo|hour|hr|pa)\b|\s?(?:p\.?a\.?|lpa|per annum))?)")
MONTHS = {m.lower(): i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}


def load_profile():
    return yaml.safe_load((ROOT / "profile.yaml").read_text(encoding="utf-8"))


def load_manual():
    p = ROOT / "data" / "manual_enrichment.csv"
    out = {}
    if p.exists():
        for r in csv.DictReader(p.open(encoding="utf-8")):
            if r.get("id") and r.get("field") and r.get("value"):
                out.setdefault(r["id"], {})[r["field"]] = (r["value"], r.get("source", "manual"))
    return out


def _sentences(t):
    return [s.strip() for s in re.split(r"[\n\r•·]+|(?<=[.;])\s+", t) if s.strip()]


def _years(text, title):
    cands = []
    for rx in YEARS_PATTERNS:
        for m in rx.finditer(text):
            if not EXP_CTX.search(text[max(0, m.start() - 40): m.end() + 70]):
                continue
            g = [int(x) for x in m.groups() if x]
            if not g or g[0] > 20:
                continue
            lo, hi = g[0], (g[1] if len(g) > 1 and g[1] >= g[0] else None)
            if lo == 0:
                continue
            consult = bool(CONSULT_NEAR.search(text[max(0, m.start() - 60): m.end() + 90]))
            cands.append((lo, hi, consult))
    if not cands:
        return None, None, False, False
    mins = sorted({c[0] for c in cands})
    split = len(mins) > 1
    # split tiers ("1-3 Consultant, 3-6 Senior Consultant"): pick the tier matching the title
    pick = mins[-1] if (split and re.search(r"(?i)senior|lead|principal", title or "")) else mins[0]
    row = next(c for c in cands if c[0] == pick)
    return pick, row[1], split, any(c[2] for c in cands if c[0] == pick)


DEG_RANK = {"Bachelor": 0, "Master": 1, "PhD": 2}


def _degree(text):
    """A sentence listing several levels ("PhD or master's", "MBA, PhD") is any-of, so its requirement is
    the LOWEST level named. Across sentences the requirement is the highest of those minimums."""
    req = pref = None
    hits = []  # (lowest level named in the sentence, is_preferred)
    for s in _sentences(text):
        lvls = [lvl for lvl, rx in DEGREE_LEVELS if re.search(rx, s)]
        if not lvls and re.search(r"(?i)\b(degree|graduate)\b", s):  # bare "degree" means bachelor only if nothing higher is named
            lvls = ["Bachelor"]
        if lvls:
            hits.append((min(lvls, key=DEG_RANK.get), bool(PREF.search(s) and not MUST.search(s))))
    # a bullet list of 4+ qualification lines ("Master of X / Master of Y / PhD in Z / Diploma") is an any-of list
    listed = [l for l, p in hits if not p]
    if len(listed) >= 4 and len(set(listed)) > 1:
        return min(listed, key=DEG_RANK.get), None
    for low, is_pref in hits:
        if is_pref:
            pref = low if pref is None or DEG_RANK[low] > DEG_RANK[pref] else pref
        else:
            req = low if req is None or DEG_RANK[low] > DEG_RANK[req] else req
    return req, pref


def _date(s):
    s = s.strip(" .,:;")
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return m.group(0)
    m = re.search(r"(?i)(\d{1,2})(?:st|nd|rd|th)?\s+([a-z]{3})[a-z]*\.?,?\s+(\d{4})", s) or None
    if m:
        d, mon, y = int(m.group(1)), MONTHS.get(m.group(2).lower()), int(m.group(3))
    else:
        m = re.search(r"(?i)([a-z]{3})[a-z]*\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})", s)
        if not m:
            return None
        mon, d, y = MONTHS.get(m.group(1).lower()), int(m.group(2)), int(m.group(3))
    try:
        return datetime(y, mon, d).strftime("%Y-%m-%d") if mon else None
    except ValueError:
        return None


EN_STOP = {"the", "and", "of", "to", "for", "with", "you", "our", "is", "are", "will", "your", "a", "an", "on", "as", "we"}


def _is_english(text):
    """True unless the JD is clearly in another language (short or empty text passes).
    ponytail: stopword ratio, English JDs sit ~0.2, Dutch/German/French ~0.02; use a language detector if mixed JDs misfire."""
    words = re.findall(r"[a-zà-ÿ]+", text.lower())
    return len(words) < 80 or sum(w in EN_STOP for w in words) / len(words) >= 0.06


def extract(row):
    text = " ".join(str(row.get(k) or "") for k in ("jd_text",)) or " ".join(
        str(row.get(k) or "") for k in ("summary", "qualifications_required"))
    title = row.get("title") or ""
    g = {}
    g["years_min"], g["years_max"], g["years_split"], g["exp_consulting_required"] = _years(text, title)
    g["degree_required"], g["degree_preferred"] = _degree(text)
    g["pedigree_terms"] = sorted({"school: " + m.group(0).lower() for m in PED_SCHOOL.finditer(text)} |
                                 {"employer: " + m.group(0).lower() for m in PED_EMPLOYER.finditer(text)})
    certs, langs = {}, {}
    for s in _sentences(text):
        found = {m.group(0) for m in CERT.finditer(s)}
        if CA_BARE.search(s) and CA_CTX.search(s):
            found.add("CA")
        for c in found:
            lvl = "preferred" if (PREF.search(s) and not MUST.search(s)) else ("required" if MUST.search(s) else "listed")
            if certs.get(c) in (None, "preferred"):
                certs[c] = lvl
        if LANG.search(s):
            lvl = "preferred" if LANG_PREF.search(s) else ("required" if re.search(r"(?i)fluen|native|proficien|essential|mandatory|must|required", s) else "listed")
            for n in LANG_NAME.findall(s):
                n = n.lower()
                if langs.get(n) in (None, "preferred", "listed") and not (lvl != "required" and langs.get(n) == "required"):
                    langs[n] = lvl
    g["certs"] = certs
    g["languages"] = langs  # name -> required | preferred | listed
    for n in re.findall(r"(?i)\b(\w+)[- ]speaking\b", title):  # "Fellow - Dutch Speaking"
        if LANG_NAME.fullmatch(n):
            langs[n.lower()] = "required"
    g["languages_required"] = sorted(n for n, l in langs.items() if l == "required")
    g["jd_english"] = _is_english(text)
    if AUTH_NOT.search(text):
        g["work_auth_stated"] = "sponsorship-not-offered"
    elif AUTH_CLEAR.search(text):
        g["work_auth_stated"] = "clearance-required"
    elif AUTH_OFFER.search(text):
        g["work_auth_stated"] = "support-offered"
    elif AUTH_RTW.search(text):
        g["work_auth_stated"] = "right-to-work-required"
    else:
        g["work_auth_stated"] = ""
    g["early_careers_role"] = bool(GRAD_ROLE.search(text)) or bool(GRAD_ROLE.search(title))
    fm = GRAD_FUTURE.search(text) or GRAD_FUTURE.search(title)
    g["grad_future_required"] = fm.group(0)[:90] if fm else ""
    dl = None
    for rx in DEADLINE:
        for m in rx.finditer(text):
            dl = _date(m.group(1))
            if dl:
                break
        if dl:
            break
    g["deadline_parsed"] = dl
    m = SALARY.search(text)
    g["salary_parsed"] = m.group(1).strip() if m and re.search(r"\d{3,}|\d\s?(?:k|lpa|lakh|l\b|m\b|million)", m.group(1), re.I) else None
    return g


def judge(row, g, prof):
    """Return (verdict, reasons[list], per-gate dict). Reasons name the actual obstacle."""
    gates, reasons = {}, []
    rank = {"CLEAR": 0, "RISK": 1, "BLOCKED": 2}
    worst = "CLEAR"

    def mark(gate, level, why):
        nonlocal worst
        gates[gate] = level
        if level != "CLEAR":
            reasons.append(f"{level} {gate}: {why}")
            if rank[level] > rank[worst]:
                worst = level

    # work authorisation: held > explicit JD statements > friendly market > route to verify. Country alone never BLOCKS (2026-10-29).
    craw = str(row.get("country") or "")
    ctry = {c.strip().lower() for c in re.split(r"[;/]", craw) if c.strip()}
    ok = {c.lower() for c in prof.get("work_authorised", [])}
    verify = set(prof.get("sponsorship_verify_countries", []))
    local = set(prof.get("local_language_countries", []))
    friendly = set(prof.get("sponsorship_friendly_countries", []))
    routes = prof.get("sponsorship_routes", {})
    st = g["work_auth_stated"]
    held = bool(ctry & ok) or any(re.search(rf"\b{re.escape(o)}\b", craw.lower()) for o in ok)  # "Multiple (... India offices ...)"; not "Indiana"
    route = "; ".join(sorted({routes.get(c) or (routes.get("_local_language") if c in local else "") or "" for c in ctry} - {""}))
    row["visa_note"] = ""
    if held:
        mark("visa", "CLEAR", "")
    elif st in ("sponsorship-not-offered", "clearance-required", "right-to-work-required"):
        mark("visa", "BLOCKED", f"{craw or 'overseas'} role states {st.replace('-', ' ')}")
    elif ctry & friendly:
        mark("visa", "CLEAR", "")
        row["visa_note"] = "sponsorship assumed available (" + ", ".join(sorted(ctry & friendly)) + (")" if st != "support-offered" else "; JD offers support)")
    elif st == "support-offered":
        mark("visa", "CLEAR", "")
        row["visa_note"] = "JD states visa/relocation support" + (f"; verify: {route}" if route else "")
    elif ctry and ctry <= (verify | local):
        mark("visa", "RISK", f"{craw}: sponsorship not stated; verify route: {route or 'see profile.yaml'}")
        row["visa_note"] = route
    else:
        mark("visa", "RISK", f"{craw or 'country unknown'}: not classified in profile.yaml, verify sponsorship")

    # years of experience
    ymin = g["years_min"]
    exp, margin = prof["paid_experience_years"], prof.get("years_risk_margin", 1.5)
    if ymin is None:
        mark("years", "CLEAR", "")
        gates["years"] = "UNSTATED"
    elif ymin <= exp:
        mark("years", "CLEAR", "")
    elif ymin <= exp + margin:
        mark("years", "RISK", f"asks {ymin}+ yrs, you have ~{exp}")
    elif g["years_split"]:  # several tiers quoted in one JD; cannot be sure which applies to this title
        mark("years", "RISK", f"quotes tiers up to {ymin}+ yrs, you have ~{exp}; split tiers, verify which applies")
    else:
        mark("years", "BLOCKED", f"asks {ymin}+ yrs, you have ~{exp} (gap {round(ymin - exp, 1)})")
    if g["exp_consulting_required"] and ymin and ymin >= 2:
        c = prof.get("consulting_experience_years", 0)
        if c < ymin:
            mark("consulting_exp", "RISK", f"needs {ymin}+ yrs IN consulting; countable ~{c} (contested)")
        else:
            mark("consulting_exp", "RISK", f"needs {ymin}+ yrs in consulting; counts only if both roles read as advisory")

    # degree
    order = ["Bachelor", "Master", "PhD"]
    have = order.index(prof.get("highest_degree", "Master"))
    rq = g["degree_required"]
    if rq and order.index(rq) > have:
        mark("degree", "BLOCKED", f"requires {rq}")
    else:
        mark("degree", "CLEAR", "")

    # pedigree language
    if g["pedigree_terms"]:
        mark("pedigree", "RISK", "screens on school/academic standing: " + ", ".join(g["pedigree_terms"][:3]))
    else:
        mark("pedigree", "CLEAR", "")

    # certifications
    held = " ".join(prof.get("certifications", [])).lower()
    miss_req = [c for c, lvl in g["certs"].items() if lvl == "required" and c.lower() not in held]
    miss_other = [c for c, lvl in g["certs"].items() if lvl == "listed" and c.lower() not in held]
    if miss_req:
        mark("cert", "BLOCKED", "required: " + ", ".join(miss_req))
    elif miss_other:
        mark("cert", "RISK", "named, not marked optional: " + ", ".join(miss_other))
    else:
        mark("cert", "CLEAR", "")

    # language: decided by the JD, not the country. A JD written in another language is a de facto requirement.
    langs = {l.lower() for l in prof.get("languages", [])}
    need = [l for l in g["languages_required"] if l not in langs]
    soft = [l for l, lv in g["languages"].items() if lv != "required" and l not in langs]
    if need:
        mark("language", "BLOCKED", "requires " + ", ".join(need))
    elif not g["jd_english"]:
        mark("language", "BLOCKED", "JD is written in a language other than English")
    elif soft:  # named as preferred/asset only: not a screen for an English-only candidate, so note it, don't flag it
        mark("language", "CLEAR", "")
        row["visa_note"] = (row.get("visa_note") + "; " if row.get("visa_note") else "") + "preferred languages not held: " + ", ".join(soft)
    else:
        mark("language", "CLEAR", "")

    # early careers: the ROLE type is fine; only a window that needs FUTURE graduation / current-student status excludes a graduate
    if g["grad_future_required"]:
        mark("early_careers", "BLOCKED", "requires future graduation or current-student status: \"" + g["grad_future_required"].replace("\n", " ") + "\"")
    else:
        mark("early_careers", "CLEAR", "")
    return worst, reasons, gates


def enrich_row(row, prof, manual):
    g = extract(row)
    verdict, reasons, gates = judge(row, g, prof)
    row["years_min"], row["years_max"] = g["years_min"], g["years_max"]
    row["years_split"] = "yes" if g["years_split"] else ""
    row["degree_required"] = g["degree_required"] or ""
    row["degree_preferred"] = g["degree_preferred"] or ""
    row["pedigree_terms"] = ", ".join(g["pedigree_terms"])
    row["work_auth_stated"] = g["work_auth_stated"]
    row["early_careers_role"] = "yes" if g["early_careers_role"] else ""
    row["gate_verdict"] = verdict
    row["gate_reasons"] = " | ".join(reasons)
    for k in ("visa", "years", "degree", "pedigree", "cert", "language", "early_careers", "consulting_exp"):
        row["gate_" + k] = gates.get(k, "")
    if not row.get("deadline") and g["deadline_parsed"]:
        row["deadline"], row["deadline_source"] = g["deadline_parsed"], "jd-text"
    if not row.get("salary_posted") and g["salary_parsed"]:
        row["salary_posted"], row["salary_source"] = g["salary_parsed"], "jd-text"
    for field, (val, src) in manual.get(row["id"], {}).items():  # manual lookups always win
        row[field] = val
        row[field + "_source"] = src or "manual"
    return row


def write_queue(rows):
    """Salary is per firm + band + country, not per posting: one lookup serves many rows."""
    groups = {}
    for r in rows:
        if r.get("salary_posted"):
            continue
        k = (r["firm"], r.get("band"), r.get("country"))
        e = groups.setdefault(k, {"n": 0, "title": r["title"], "url": r["url"], "verdict": set()})
        e["n"] += 1
        e["verdict"].add(r.get("gate_verdict"))
    p = ROOT / "data" / "enrichment_queue.csv"
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["firm", "band", "country", "n_roles", "worth_looking_up", "example_title", "example_url",
                    "salary_source_hint", "found_value", "found_source"])
        for (firm, band, ctry), e in sorted(groups.items(), key=lambda kv: -kv[1]["n"]):
            worth = "yes" if e["verdict"] & {"CLEAR", "RISK"} else "no (all BLOCKED)"
            hint = "AmbitionBox / Glassdoor India" if (ctry or "").lower() == "india" else "Glassdoor / Levels.fyi / Payscale"
            w.writerow([firm, band, ctry, e["n"], worth, e["title"], e["url"], hint, "", ""])
    return p, len(groups)


def _selftest():
    prof = {"paid_experience_years": 4.0, "years_risk_margin": 0, "consulting_experience_years": 2.75,
            "work_authorised": ["India"], "languages": ["English"], "highest_degree": "Master", "certifications": [],
            "sponsorship_verify_countries": ["united kingdom", "united states", "canada"],
            "local_language_countries": ["germany", "france", "netherlands"], "sponsorship_friendly_countries": ["uae", "singapore"],
            "sponsorship_routes": {"united states": "H-1B or L-1", "_local_language": "Blue Card"}}
    base = {"id": "x", "country": "India", "title": "Consultant", "firm": "F", "url": "u", "band": "Consultant"}
    t = lambda **kw: enrich_row({**base, **kw}, prof, {})
    r = t(jd_text="Master's degree from a reputable University. 1-3 years of experience in Big4 consulting.")
    assert r["gate_verdict"] == "RISK" and "pedigree" in r["gate_reasons"] and r["years_min"] == 1, r
    r = t(jd_text="Minimum 5 years of relevant experience in strategy. CFA is required. Apply by 15 October 2026.")
    assert r["gate_verdict"] == "BLOCKED" and r["gate_years"] == "BLOCKED" and r["gate_cert"] == "BLOCKED", r
    assert r["deadline"] == "2026-10-15", r
    r = t(country="Germany", jd_text="Fluent German required. 2 years of experience.")
    assert r["gate_visa"] == "RISK" and r["gate_language"] == "BLOCKED", r  # the JD blocks it, not the country
    r = t(country="Netherlands", jd_text="Strategy consultant, 3 years of experience. Our team works in English.")
    assert r["gate_visa"] == "RISK" and r["gate_language"] == "CLEAR" and "Blue Card" in r["visa_note"], r
    nl = ("Als strategisch adviseur werk je samen met klanten aan vraagstukken over digitale transformatie. "
          "Je hebt minimaal drie jaar ervaring in consultancy en een afgeronde masteropleiding. ") * 6
    r = t(country="Netherlands", jd_text=nl)
    assert r["gate_language"] == "BLOCKED", r  # a JD written in Dutch needs Dutch
    r = t(country="Netherlands", title="Fellow - Dutch Speaking", jd_text="3 years of experience.")
    assert r["gate_language"] == "BLOCKED", r
    r = t(country="United States", jd_text="3 years of experience in analytics.")
    assert r["gate_visa"] == "RISK" and "H-1B" in r["visa_note"], r
    r = t(country="United Kingdom", jd_text="Visa sponsorship is available. 3 years of experience in analytics.")
    assert r["gate_visa"] == "CLEAR", r  # stated support clears it; the register check still runs at Stage -1
    r = t(country="Indiana; United States", jd_text="3 years of experience.")
    assert r["gate_visa"] == "RISK", r  # "india" inside "Indiana" is not India
    r = t(country="UAE", jd_text="3 years of experience in analytics.")
    assert r["gate_visa"] == "CLEAR" and "assumed" in r["visa_note"], r
    r = t(country="Singapore", jd_text="You must have the right to work in Singapore. 3 years of experience.")
    assert r["gate_visa"] == "BLOCKED", r  # explicit right-to-work statement beats the assumption
    r = t(country="Pakistan", jd_text="3 years of experience.")
    assert r["gate_visa"] == "RISK", r
    r = t(country="Thailand; Singapore", jd_text="3 years of experience.")
    assert r["gate_visa"] == "CLEAR", r
    r = t(title="Senior Consultant", jd_text="1-3 years for Consultant and 4-6 years for a Senior Consultant of experience in consulting.")
    assert r["years_min"] == 4 and r["years_split"] == "yes", r
    r = t(jd_text="Join our graduate programme. Preferred: CFA. Salary range ₹12,00,000 - ₹15,00,000 per annum.")
    assert r["gate_early_careers"] == "CLEAR" and r["early_careers_role"] == "yes", r  # scheme itself is fine
    assert r["gate_cert"] == "CLEAR" and "12,00,000" in r["salary_posted"], r
    r = t(jd_text="Associate Consultant graduate programme. Candidates must be graduating by September 2027.")
    assert r["gate_early_careers"] == "BLOCKED", r  # needs FUTURE graduation, a completed graduate cannot meet it
    r = t(jd_text="Open to recent graduates who completed a degree in the last 12 months. 2 years of experience.")
    assert r["gate_early_careers"] == "CLEAR", r
    # regressions found by auditing real JDs: nav boilerplate and any-of lists must not block
    r = t(jd_text="Similar jobs: Consulting DE, Consulting CN, Consulting CA. EXPERIENCED TALENT EARLY CAREERS TALENT. 3 years of experience in analytics.")
    assert r["gate_cert"] == "CLEAR" and r["gate_early_careers"] == "CLEAR", r
    r = t(jd_text="Your background: PhD or master's degree with several years of work experience in life sciences.")
    assert r["degree_required"] == "Master" and r["gate_degree"] == "CLEAR", r
    r = t(jd_text="Proficiency in English (essential) together with French, Italian, or Spanish. Priority given to French speakers.")
    assert r["gate_language"] == "CLEAR" and "french" in r["visa_note"], r  # preferred, not required: noted only
    r = t(jd_text="Educational qualifications: MBA / PGDBM / CFA/CA. 3 years of experience.")
    assert r["gate_cert"] == "RISK", r
    r = t(jd_text="Qualifications:\n- Master of Business Administration\n- Master of Computer Applications\n- PhD in Economics\n- Post Graduate Diploma in Management\n- Bachelor of Technology")
    assert r["gate_degree"] == "CLEAR" and r["degree_required"] == "Bachelor", r
    r = t(jd_text="Candidates with a top tier consulting firm background and a strong academic record.")
    assert "employer: top tier consulting firm" in r["pedigree_terms"] and r["gate_pedigree"] == "RISK", r
    print("enrich selftest OK")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        sys.exit(__doc__)
