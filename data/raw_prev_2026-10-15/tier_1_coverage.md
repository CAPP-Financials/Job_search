# Tier 1 coverage (McKinsey, BCG, Bain) - swept 2026-10-15, window posted_date >= 2026-10-08

- **McKinsey & Company**
  - Method: portal's own JSON gateway, `GET https://gateway.mckinsey.com/apigw-x0cceuow60/v1/api/jobs/search?pageSize=100&start=<page 1..7>&lang=en` (plain `requests`, no Firecrawl). Each doc carries whoYouWillWorkWith / whatYouWillDo / yourBackground, used as the full JD.
  - Postings seen: 622 (numFound 622, 7 pages, unique jobIDs). Kept: 44.
  - Date caveat: the portal exposes NO posted date. Only `postedToLinkedInDate` exists and is used as a proxy (source "portal") when it falls inside 2026-10-08..2026-10-15: 113072 (10-09), 113124 (10-13), 113180 (10-13), 113127 (10-12), 113184 (10-15). 39 kept roles are undated evergreen requisitions (posted_date null, source "none"); 3 Knowledge Analyst roles (113266/113267/113269) carry a future LinkedIn date (2026-10-16) and were stored undated.
  - Dropped vs the 10-10 sweep: 102501 (LinkedIn date 10-05, now outside window); 101141, 101348, 111671 no longer on the portal. 113096 Associate - Transformation (new, undated) dropped for a 6+ yrs ask.
  - Excluded after title/JD review: Manager/EM/AP/Director/Principal, QuantumBlack engineers/data scientists, interns, finance/HR/legal/admin/IT/helpdesk, Client Development Advisor, Client Activation Specialist, Senior Expert, Knowledge Expert.
  - Back-end ATS: Avature (`jobApplyURL` = `mckinsey.avature.net/careers/ApplicationMethods?folderId=<id>`), front end Sitecore + Next.js.
- **BCG**
  - Method: Eightfold JSON API, `GET https://experiencedtalent.bcg.com/api/apply/v2/jobs?domain=bcg.com&start=<n>&num=100` (the API returns ~10 per call, so paginated by returned count), detail via `/api/apply/v2/jobs/<id>?domain=bcg.com`. Date = `t_create` epoch (portal date).
  - Postings seen: 673 unique (portal count 675). In window (>= 10-08): 52. Kept: 4 (60106 Senior Analyst Corporate Finance & Strategy, SF, 10-09; 60224 Delivery AI Product Analyst, Chicago, 10-13; 60189 Consultant Operations-Procurement, Germany, 10-12; 60192 Traditional Consulting Experienced Consultant, Germany, 10-12).
  - Near misses, not kept: 60098 Lead AI Tech Architect Amsterdam (10-15 yrs); 60248 Platinion Lead/Principal AI Tech Consultant (Principal band); 60211 Nordic Data & Analytics Specialist (up to 3 yrs, data/analytics support, band not in scope); 60214/60225 marketing analytics specialists; 60234 BCG X Finance Analyst; 60099 Sustainability Data & Analytics Senior Manager (Manager+); 59977 AI Tech Consultant (10-06, outside window now). Rest of in-window portal is Manager+/director/engineer/intern/HR/admin. No sustainability-track (B) role at kept bands.
  - Back-end ATS: Eightfold (`careers.bcg.com` is a Phenom front end handing off to experiencedtalent.bcg.com/careerhub).
- **Bain & Company**
  - Method: portal JSON, `GET https://www.bain.com/en/api/jobsearch/keyword/get?start=<page 0..>` (10 per page). Needs `Referer: https://www.bain.com/careers/find-a-role/` and `X-Requested-With: XMLHttpRequest` headers, otherwise returns "Forbidden: Direct API access is not allowed". Each `.../position/?jobid=<id>` page supplies JSON-LD `datePosted` and the full description.
  - Postings seen: 309 (totalResults 309). In window (datePosted >= 10-08): 23. Kept: 6 = 110467 Associate BCN TMT (Mexico City, 10-09), 111280 Associate (CE) Customer CoE (New Delhi, 10-13), 111215 Associate (Procurement) Performance Improvement CoE (New Delhi, 10-12), plus undated evergreen 10397 Associate Consultant, 10409 Consultant, 10433 Junior Consultant (Bengaluru/Mumbai/New Delhi, new vs 10-10).
  - Not kept: 110771-110774 Vector Associates (10-05, outside window now); 110769 IIT Delhi DMS Associate Batch of 2027 (campus-only programme); 111257 Analyst TSG Product Management (internal tech product role); 111173 Senior Associate Full stack + AI, TSG engineers, AI Engineering Manager/Lead, Project Leaders, Managers, recruiting/HR/finance/ops, student/working-student, programmes and scholarships (undated programme pages).
  - Back-end ATS: Avature (`careers.bain.com/jobs/Login?folderId=<id>`, avacdn assets).

## Cross-cutting notes
- Nothing signed in, no forms submitted, no accounts created. Firecrawl calls used: 0.
- Track A/B tagging is heuristic (B only if sustainability terms dominate); 103160 and 60189 tagged AB. No pure B role at kept bands.
- Intermediate dumps (full portal lists, position pages) were kept in the session scratchpad, not in the repo.
