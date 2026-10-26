# Tier 1 coverage (McKinsey, BCG, Bain) - swept 2026-10-21, window posted_date >= 2026-10-14

Kept 52 = McKinsey 46, BCG 3, Bain 3. Scope detail (global / UK / India / other markets) is in tier_1_scopes.json. All three firms run one global portal that lists UK and India offices, so UK and India are "via-global" with posting ids cited; nothing signed in, no forms submitted, Firecrawl calls used: 0.

- **McKinsey & Company**
  - Method: portal JSON gateway `GET https://gateway.mckinsey.com/apigw-x0cceuow60/v1/api/jobs/search?pageSize=100&start=<1..7>&lang=en` (plain requests). whoYouWillWorkWith / whatYouWillDo / yourBackground used as the JD.
  - Seen 614 (7 pages, unique jobIDs; was 622). Kept 46. UK: 44 seen / 3 kept (15178, 15136, 20159). India: 51 seen / 1 kept (20159). Gulf/APAC/ZA: UAE 11/3, Saudi 18/6, Qatar 17/6, Singapore 15/4, Hong Kong 8/3, Malaysia 8/4, South Africa 20/5, Philippines 9/3 (seen/kept; global-wide reqs count in several countries).
  - Date caveat: no posted date on the portal. `postedToLinkedInDate` is the proxy (source "portal") when it falls in 2026-10-14..2026-10-21. 122 portal reqs have no LinkedIn date; consulting-type ones are kept as undated evergreen (posted_date null, source "none").
  - Newly kept vs 10-15: 20159 Junior Associate (global incl. UK, India, Gulf), 113201 Associate Strategy & Corporate Finance (DACH, German), 113385 Consultant Energy (10-21, Argentina/Chile), 113386 Consultant Energy O&G (10-21, 5+ yrs), 113384 Consultant Metals & Mining (10-21, 5+ yrs), 113281 Consultant Tech & AI Seoul (10-16, 5+ yrs preferred), 113396 Senior Delivery Consultant Public Sector Saudi (undated, 4+ yrs). Knowledge Analyst 113266/113267/113269 now carry a real 10-16 date.
  - Dropped vs 10-15: 113124, 113072, 113180, 113127 (LinkedIn dates 10-09..10-13, now before window); 111966 gone from portal.
  - Excluded: 113096 Associate Transformation (6+ yrs), 112634 Senior Client Success Analyst Wave (client success, not consulting), 106398 research fellow (PhD), Manager/EM/AP/Director/Principal, QuantumBlack engineers/data scientists, interns, finance/HR/legal/admin/IT/recruiting, Client Development Advisor, Client Activation Specialist, Knowledge/Senior Expert, India back-office reqs (Finance, Knowledge, Ops, Product Analyst Periscope).
  - ATS: Avature (`mckinsey.avature.net/careers/ApplicationMethods?folderId=<id>`). Dedicated www.mckinsey.com/gb/careers and /in/careers reset the connection from this client; they front the same gateway.
- **BCG**
  - Method: Eightfold JSON API `GET https://experiencedtalent.bcg.com/api/apply/v2/jobs?domain=bcg.com&start=<n>&num=100` plus detail `/api/apply/v2/jobs/<id>?domain=bcg.com`; date = `t_create`. careers.bcg.com is the Phenom front end for the same board.
  - Seen 676; 41 dated >= 10-14. UK 109 seen / 6 in window / 1 kept; India 104 / 7 / 0; UAE 3, Saudi 17, Qatar 1, Singapore 11, Hong Kong 5, Malaysia 24, South Africa 4, Philippines 6 (seen; 0 kept).
  - Kept 3: 2026-60331 Delivery AI Product Analyst UK BCG X (London, 10-20, 2-3 yrs); 2026-60263 Consultant Transform Practice (Germany/Austria, 10-16, 3-5 yrs, German+English); 2026-60253 AI Tech Associate Athens BCG Platinion (10-15, 2 yrs IT consulting, Greek+English).
  - Dropped vs 10-15 (dated before window now): 60106, 60224, 60189, 60192. Not kept in window: 60252 Senior Experienced Rapid Value and Cash (12-20+ yrs), 60305 (Senior) AI Tech Architect Greater China (architect, not in band), 60234 BCG X Finance Analyst (finance), Platinion Principal/Lead, Project Leaders, IT directors, HR/recruiting/interns. 60262/60240 etc India reqs are Manager+/engineering/HR. No B-track role at kept bands.
- **Bain & Company**
  - Method: portal JSON `GET https://www.bain.com/en/api/jobsearch/keyword/get?start=<page>` (needs Referer `https://www.bain.com/careers/find-a-role/` and `X-Requested-With: XMLHttpRequest`), JSON-LD `datePosted` + description from each `.../position/?jobid=<id>` page for all 304.
  - Seen 304; 10 dated >= 10-14, none a kept-band consulting role. UK 29 seen / 0 in window / 2 kept; India 96 / 4 in window / 3 kept; UAE 11, Saudi 10, Qatar 9, Singapore 7, Hong Kong 5, Malaysia 14, South Africa 1, Philippines 5 (evergreen multi-office reqs 10397/10409 appear in most).
  - Kept 3 undated evergreen: 10397 Associate Consultant, 10409 Consultant, 10433 Junior Consultant (Bengaluru, Mumbai, New Delhi).
  - Dropped vs 10-15: 110467, 111280, 111215 (dated 10-09..10-13, before window). Near misses not kept: 110541 Practice Consultant Integrated Operations Lisbon (10-19; internal practice role, 5-8 yrs / MBA + 4-5), 110264 Senior Analyst PPK Operations New Delhi (10-16; internal automation builder), 111374 Project Leader, 111346 travel associate, 110069 QA engineer; programmes, scholarships, interns, engineers, HR/recruiting/finance/ops.
  - ATS: Avature (`careers.bain.com`).

## Notes
- Track A/B tagging is heuristic; AB on McKinsey 113385/113386/113384 and 103160 (energy/materials). No pure B role at kept bands.
- Intermediate dumps kept in the session scratchpad, not the repo.
