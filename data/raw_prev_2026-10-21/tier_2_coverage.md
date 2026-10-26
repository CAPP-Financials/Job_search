# Tier 2 coverage (Big Four arms), run 2026-10-21, window posted_date >= 2026-10-14

Output: tier_2.jsonl, 172 roles (EY careers 65, EY-Parthenon 20, PwC global 34, PwC India 16, Strategy& 2, PwC UK 1, PwC Middle East 1, Deloitte global portal 16 [US 5, Southeast Asia 11], Deloitte Middle East 5, Deloitte UK 1, Deloitte USI 1, KPMG India 7, KPMG global 3 [Singapore], KPMG UK 0, Monitor Deloitte 0). Every record carries the full JD text as fetched. Machine-readable scope proof is in tier_2_scopes.json (global / uk / india / other per firm, with url, seen, kept, note).

Method: all lists read from the firms' own boards over plain HTTP/APIs (no Firecrawl for sweeps; fc.py search used only to locate Deloitte Southeast Asia and Southern Africa boards). Title filter first (band words: analyst, associate, consultant, advisor, strategy; dropped Manager+/director/partner/lead/intern/graduate and cyber, tax, audit, risk, forensic, SAP/Oracle/Salesforce/ServiceNow/Workday/Dynamics, developers/engineers/architects, valuation/diligence, finance operations, HR/legal/admin), then detail fetch for the date and JD, then manual pick of consulting-type roles. Asks of 6+ years dropped (EY 8, PwC 3). Duplicate re-posts (same title and location) collapsed with the extra req ids appended to jd_text. Track A/B/AB, years_exp, qualifications and keywords are heuristics from JD text.

## Scope table (seen / kept)
Firm | global | uk | india
- Deloitte (global portal): apply.deloitte.com 1,449 rows read, 29 date-checked, 5 kept; jobs.sea.deloitte.com 766 rows, 11 kept | UK see Deloitte UK | India see Deloitte USI
- Deloitte USI (India): usijobs.deloitte.com 615 rows, 1 kept
- Deloitte UK: apply.deloitte.co.uk 601 rows (45 in window), 1 kept
- Deloitte Middle East: middleeastjobs.deloitte.com 173 pipelines (11 in window), 5 kept
- Monitor Deloitte: no separate board; 0 titles across all five Deloitte lists
- PwC global/UK/India/Strategy&: one Workday tenant. Global_Experienced_Careers 3,862 + CRM_Experienced_Careers_Site 1,736 postings, 960 rows paged newest-first, 679 dated in window (India 285, UK 22, Egypt 27, Singapore 6, Malaysia 7, South Africa 10, Philippines 23). 138 passed the title filter, 54 kept. UK also read on jobs.pwc.co.uk (Phenom, 336 postings, 26 in window).
- PwC Middle East: pwc.com/m1 (Playwright), 493 Egypt ETIC Workday rows + 69 SuccessFactors rows; 1 kept.
- Strategy&: Workday (2 kept), Germany Phenom 45 (0 in window), Middle East Greenhouse 17 (0 in band in window).
- EY careers (global) and EY-Parthenon: one SuccessFactors board. 4,000 rows read, 2,850 in window (GB 110, IN 915); 412 detail-fetched; 85 kept (India 25, UK 1).
- KPMG India: Oracle HCM CX_3, 570 total, 200 read, 116 in window, 7 kept.
- KPMG UK: 147 vacancies, no dates, 0 in band.
- KPMG global: routes to member sites. UAE (Oracle HCM, 76 total, newest 2026-10-13), Saudi Arabia (6), Singapore (180 with dates, 32 in window, 3 kept).

## Blockers and gaps
- Deloitte Hong Kong / China: ehjobs.deloitte.com.cn is a JS app, not read (blocked).
- KPMG Qatar (HTTP2 protocol error) and KPMG South Africa (Taleo JS, timed out): blocked. KPMG Malaysia, Philippines and Hong Kong: member career pages expose no job board (none).
- PwC Hong Kong, Qatar, UAE, Saudi on Workday: no postings in window; pwc.com/m1 SuccessFactors dates are page-build dates so in-band candidates were date-checked on job pages (all out of window or UAE-nationals-only).
- Deloitte US board has no list dates and a 10-per-page cap; only title-shortlisted ids >= 370800 were date-checked (29). US reqs with future datePosted (2026-11-30 to 2026-12-26) were ignored as unreliable. Portal returned HTTP 200 throughout this run (no 406s) with 1 to 1.5 s spacing.
- EY list has no dates; in-window boundary found by sampling (row 2,500 to 2,750 is 2026-10-14), so a few 2026-10-13/14 rows near the boundary could be missed or included only if title-shortlisted and individually dated.
- Several Deloitte USI "EH-FY27-Consulting-S&T-Strategy" Senior Consultant reqs and Strategy& Germany Senior Associate reqs are long-running evergreen postings but carry portal dates before the window (May to Sept 2026, Nov 2025), so they are not kept.
- Shared Chromium/Python browser downloads were not used except Playwright for pwc.com/m1 and slccareers.kpmg.com.

## Caveats
- Deloitte US and some UK roles require US work authorisation or SC/TS clearance (flags in summary). Deloitte Middle East and some Deloitte SEA/PwC roles are national- or language-restricted (German-speaker ETIC roles dropped).
- Sponsorship flag: n/a-local for India postings, likely-needed elsewhere (country based, not stated per JD).
- Non-English JDs (German, French, Dutch, Spanish, Portuguese, Hungarian, Czech/Croatian) stored as published.
- No undated evergreen roles seen; every board exposes dates, so posted_date_source "none" does not appear.
