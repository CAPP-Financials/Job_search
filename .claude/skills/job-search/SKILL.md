---
name: job-search
description: Use when the user asks to run the job search, find consulting roles from firm career portals, or filter the tracker by visa, language, years, degree, keyword etc. Filters are opt-in: a filter applies only if named.
---

# job-search

Roles come from firm career portals only (firms/firms.yaml, 77 firms, tiers 1, 2, 3A, 3B, 3C). Bands: Analyst to Senior Consultant, 2-5 yrs, last 7 days.

## Filters are opt-in

`/job-search` with nothing else = window + band only, no gate filtering.
Each word the user adds turns ONE filter on. A role must pass every filter that is on.

| User says | Flag | Drops |
|---|---|---|
| visa, sponsorship | `--visa` | UK/US/CA/AU/NZ/IE regime roles, JD says no sponsorship / clearance / right-to-work |
| language | `--language` | JD requires a language not held, or language-barrier country |
| years, experience | `--years` | JD asks more years than profile.yaml (unstated years pass, tagged "years unstated") |
| degree | `--degree` | requires higher degree than held. Degree requirement is read from each JD itself; the run prints what the kept roles ask for |
| pedigree | `--pedigree` | yes/no: asks for a top-tier / Ivy / IIM-ISB-class school (grade language and prior-employer pedigree are not school tier) |
| cert | `--cert` | required certification not held |
| early careers | `--early-careers` | needs future graduation / current-student status |
| keywords exact / fuzzy | `--keywords exact` or `--keywords fuzzy` | role must hit >= `min_hits` terms from `keywords.yaml` (its track's list). Fuzzy tolerates spelling and plural variants. No need to state a count |
| semantic | `--semantic` | yes/no: JD must meet the embedding-similarity bar vs the matching resume (`semantic_min` in `keywords.yaml`) |
| keyword "X" | `--keyword "X"` | exact whole-word phrase X must be in title or JD; repeat = all must match |
| any of "X", "Y" | `--any-keyword X --any-keyword Y` | at least one phrase present |
| strict | `--strict` | RISK also fails (not just BLOCKED) |
| all filters | all gate flags above | a role that clears every hard gate |

Scope modifiers: `--tier 1 2`, `--firm NAME`, `--track A|B`, `--country India`, `--undated` (keep undated evergreen reqs), `--days N`.

## Run

1. Refresh data (only when the user wants a new week): sweep each tier from the portals into `data/raw/tier_*.jsonl` (back up the old ones to `data/raw_prev_<date>/` first), then
   `python -I scripts/consolidate.py --today YYYY-MM-DD`
   Writes the dated tracker `trackers/tracker_YYYY-MM-DD.xlsx` (one per run, so ~52 a year) and recomputes every gate verdict from `profile.yaml`.
2. Filter: `python scripts/filter.py --today YYYY-MM-DD <flags>`
   Adds the funnel to that dated tracker: sheet `Funnel` (counts per step), then `F0 All`, `F1 Window+Band`, one sheet per filter ON (`F2 +visa`, ...), each cumulative so the row count only shrinks, and `FINAL` = roles that cleared everything, CLEAR first then RISK. Work from FINAL.
3. Report to the user: filters ON, the Funnel counts, FINAL clear vs risk, how many have unstated years.

## Rules
- Never apply a filter the user did not name. Never silently tighten.
- Profile (years 4.0, English only, India authorised) lives in `profile.yaml`; change it there, not in code.
- Check: `python -I scripts/filter.py --selftest` and `python -I scripts/enrich.py --selftest`.
