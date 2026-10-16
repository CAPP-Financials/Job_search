# Tier sweep brief (paste into each tier agent; replace TIER and DATES)

Re-sweep every firm of tier "TIER" in firms/firms.yaml from the firm's OWN career pages. Window: posted_date >= TODAY-7. Keep undated evergreen consulting reqs (posted_date null, source "none"). Overwrite data/raw/tier_TIER.jsonl, data/raw/tier_TIER_coverage.md and write data/raw/tier_TIER_scopes.json.

Read first: previous tier_TIER_coverage.md and tier_TIER.jsonl (method + exact record schema) in the latest data/raw_prev_<date>/ folder; use scripts/fc.py as the only Firecrawl route (shared throttle; prefer plain HTTP/APIs).

## MANDATORY scope rule: global, UK and India for EVERY firm
For every firm, check three career pages and say what you found for each:
- global (the firm's main/global careers page)
- uk (its UK careers page)
- india (its India careers page)
If one portal serves several countries (e.g. an Eightfold board with a location filter), that is fine, but PROVE it: show that UK and India postings appear there ("via-global"). A global page that only routes to member-firm sites (e.g. kpmg.com) does NOT count as checked: follow it to the member firm sites.
Also sweep member firms in sponsorship-friendly markets where they exist: UAE, Saudi Arabia, Qatar, Singapore, Hong Kong, Malaysia, South Africa, Philippines (list them under "other").

Write data/raw/tier_TIER_scopes.json:
{"<firm name exactly as in firms.yaml>": {
   "global": {"status": "ok|via-global|none|blocked", "url": "...", "seen": N, "note": "evidence or reason"},
   "uk":     {...}, "india": {...},
   "other":  [{"country": "UAE", "status": "...", "url": "...", "seen": N}] }}
Statuses: ok = swept directly; via-global = the global board lists that country (cite a UK/India posting id); none = the firm has no such page (give the reason); blocked = tried and could not read (give the blocker). Never leave a scope out and never write "ok" without a URL.

Keep rules: bands Analyst, Senior Analyst, Associate, Senior Associate, Associate Consultant, Consultant, Senior Consultant; consulting-type roles; drop Manager+, partners, interns, pure engineering, HR/finance/legal/admin, asks of 6+ years. Tag track A, B or AB. Full JD in jd_text. Never sign in or submit anything.
Final message: seen/kept per firm per scope, blockers.
