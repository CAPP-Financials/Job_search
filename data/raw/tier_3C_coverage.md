# Tier 3C coverage (sweep date 2026-10-15, window posted_date >= 2026-10-08)

Format: firm | method | postings seen | kept | blocker / notes | back-end ATS evidence beyond apply vendor

- Redseer Strategy Consultants | Zoho Recruit portal https://redseer.zohorecruit.in/jobs/Careers, job JSON embedded in page + Date_Opened per JD page | 5 | 0 | Same 5 listings as last sweep: Associate Consultant (opened 2025-10-24), Senior Consultant (2025-09-02), Sector Analyst (2025-09-02), Sector Lead (2025-09-02), Writer & Editor Sr Associate (2026-08-27). All outside window. | Zoho Recruit only.
- Praxis Global Alliance | https://praxisga.hire.trakstar.com/ (via praxisga.com/join-us) | 0 | 0 | Trakstar page says "No jobs available". | Trakstar Hire.
- Avalon Consulting | https://www.consultavalon.com/work-with-us/apply-now/ | 0 | 0 | General application form only; no listings, titles or dates. | no evidence (WordPress form).
- Technopak (The Knowledge Company) | https://tkc.in/careers/ listing page | 7 | 0 | Same 7 roles as last sweep (Consulting Manager, Research Associate - Retail, Senior Associate - Retail, Digital Marketer, Marketing Manager, Senior Associate - Apparel Operations, WGSN BD Manager). In-band ones were published 2024-09 to 2025-11, outside window; page still carries a 2025 event banner (stale). | WordPress + native form.
- 1Lattice | Trakstar Hire https://1lattice.hire.trakstar.com/ listing | 24 | 0 | All Associate Director / Manager / Director / Project Manager / Account Manager BD / Chartered Accountant / Graphic Designer / PR & Events roles; no Analyst/Consultant band consulting role. No posted dates exposed. | Trakstar Hire.
- Sattva Consulting | Kula ATS page https://careers.kula.ai/sattva (plain HTTP; Next.js RSC payload contains all job objects with launch_at and full JD HTML; the old ats_job_posts JSON endpoint now returns err_invalid_type) | 61 | 5 | Kept (launch_at >= 10-08): Consultant - Education (10-09, 4-6 yrs, fixed-term), Associate Consultant Corporate Advisory Ahmedabad (10-09, 2-4, 1-yr tenure), Senior Consultant Sustainability and Business Advisory (10-09, 5-8 yrs top of band, flag), Associate Consultant Foundations Advisory Energy and EV (10-11, 2-4), Associate Consultant CSR Corporate Advisory Bengaluru (10-15, 2-4, Kannada mandatory, client-site implant). Excluded in window: Consultant, Business & Financial Operations (10-14; internal BU finance/ops role, 5-8 yrs), Engagement Manager Government Advisory (10-15, Manager). Dropped vs last sweep because now before window: Consultant Legal & Policy Advisory (10-05), Corporate Analyst Mumbai (10-07). | Kula (kula.ai).
- Nexdigm | WP page https://www.nexdigm.com/careers/current-openings/ via Playwright, LOAD MORE clicked until exhausted | 20 | 0 | Same tax, accounting, transfer pricing, market-research ops and trainee roles; no consulting-band role. No posted dates. | no evidence.
- Tredence | RippleHire https://tredence.ripplehire.com (token rzuz0vttMaz0VxxVzDiY); POST /candidate/candidatejobsearch with form field careerSiteUrlParams={"page":0,"search":"*:*","campaignSeq":"","token":..,"source":"CAREERSITE","pagesize":50}, header Accept application/json | 57 | 0 | List endpoint exposes no dates; newest req ids (915218 Sr Technical Program Manager 13-18 yrs, 913129 Data Governance Lead/Manager) are Manager+; only band-title roles are Consultant 908545 (2-5 yrs, posted 2026-09-15 per last sweep), Consultant - Analytics 882979 (0-1), Consultant 881317 (0-0), all before window. Firecrawl scrape of the portal errored ("server unavailable"), so none spent here. | RippleHire.
- Fractal Analytics | Workday CXS JSON https://fractal.wd1.myworkdayjobs.com/wday/cxs/fractal/Careers/jobs (paged, total 117) + per-job CXS detail (startDate) | 117 | 1 | In window by relative date (<= 7 days): Data Engineer - AWS, GenAI Engineer, AI Governance Architect, Support Engineer L3, Senior Consultant - Marketing Analytics (SR-46751, startDate 2026-10-13, US remote) KEPT, Program Manager GenAI (SR-45822, 8-10 yrs, dropped), Client Partner Azure, Data scientist Census, Senior Data Engineer, AI Engineer. | Workday only.
- Zinnov | Greenhouse boards-api https://boards-api.greenhouse.io/v1/boards/zinnov/jobs (first_published) | 36 | 0 | In window: nothing (2 People Success Partner interns on 10-06 are before window and out of scope). Project Lead - I (US) first_published 2026-10-01, before window. | Greenhouse.
- Everest Group | WP page https://www.everestgrp.com/careers/ + job pages (published/updated meta) | 5 | 0 | Unchanged: Senior Analyst - CIS (published 2026-07-19, updated 2026-09-03), Senior Analyst - Application Services (2025-09-15, updated 2026-07-19) in band but before window; 3 Practice Director roles out of band. | no ATS evidence; apply via LinkedIn.
- Primus Partners | https://www.primuspartners.in/jobs | 0 | 0 | "0 Results / No jobs found". | no evidence.
- Intellecap | https://www.intellecap.com/current-opportunities | 8 | 0 | All 8 listings carry 2025 deadlines (June-Sept 2025), stale; none current. | no evidence (email apply).
- Wazir Advisors | https://wazir.in/career/ (browser User-Agent needed) | 1 | 0 | Only Senior Business Consultant, Dubai (8+ yrs, relative "Posted 19 hours ago" text is unreliable, page modified 2023). Out of band. | no ATS evidence.
- Analysys Mason | SmartRecruiters public API https://api.smartrecruiters.com/v1/companies/AnalysysMason1/postings (releasedDate) | 39 | 0 | In window (>= 10-08): Principal / Director Value Creation & Strategy Frankfurt (10-08) and Internship Transaction & Strategy Consulting PE Munich (10-08), both excluded. Last sweep's four kept roles (10-05, 10-06) are now before window. | SmartRecruiters.
- Frost & Sullivan | BambooHR JSON https://frostsullivan.bamboohr.com/careers/list + /careers/{id}/detail (datePosted) | 49 | 1 | In window: Research Analyst, Cybersecurity (533, 10-13, Malaysia) KEPT as Analyst-band market research/consulting; Senior Consultant Growth Strategy & Implementation Riyadh (536, 10-15) dropped (6+ yrs, 2 yrs Gulf); MetaBrain AI Model Trainer, Assistant Manager Finance, 2 x VP Revenue Operations excluded. | BambooHR.
- Value Partners | https://www.valuepartners.com/careers (SPA; plain fetch returns shell only; last sweep via Playwright) | 0 | 0 | Only "Send your cv" CTAs for Management Consulting and Digital Technology, no listings or ATS. | no evidence.
- Elixirr | https://elixirr.com/job-openings via Playwright (31 vacancies) | 31 | 0 | Same 31 vacancies as last sweep; in-band candidates (2027 Graduate Analyst London, Consumer Insights Associate Consultant LA, Consumer Insights Senior Consultant LA, Digital Marketing Consultant London, Senior Technology Consultant Dallas/London) all dated before window per last sweep's JSON-LD datePosted; no new in-band role appeared. Talent Acquisition Consultant Dallas is HR, excluded. | Greenhouse embed.

## Corrected careers URLs (firms.yaml entries that were wrong or moved)
- Praxis Global Alliance: https://www.praxisga.com/join-us (openings at https://praxisga.hire.trakstar.com/)
- Avalon Consulting: https://www.consultavalon.com/work-with-us/apply-now/
- Technopak: https://tkc.in/careers/
- Wazir Advisors: https://wazir.in/career/
- Sattva Consulting: https://careers.kula.ai/sattva
- Intellecap: https://www.intellecap.com/current-opportunities
- Elixirr: https://elixirr.com/job-openings
- Zinnov: Greenhouse board zinnov
- Primus Partners: https://www.primuspartners.in/jobs
- Nexdigm: https://www.nexdigm.com/careers/current-openings/
- Fractal: https://fractal.wd1.myworkdayjobs.com/Careers
- Tredence: https://tredence.ripplehire.com/candidate/?token=rzuz0vttMaz0VxxVzDiY&source=CAREERSITE
- Analysys Mason: https://careers.smartrecruiters.com/AnalysysMason1
- Frost & Sullivan: https://frostsullivan.bamboohr.com/careers
- 1Lattice: https://1lattice.hire.trakstar.com/
- Redseer: https://redseer.zohorecruit.in/jobs/Careers

## Notes
- Total kept: 7 roles (Sattva 5, Frost & Sullivan 1, Fractal 1). Written to tier_3C.jsonl. Sattva's 3 roles dated 10-09 were carried from the prior sweep record unchanged.
- Firecrawl calls used: 1 (Tredence, failed with portal error). Everything else via plain HTTP, public APIs, or Playwright.
- Eligibility flags: Fractal SR-46751 is a US remote role (work authorisation needed, sponsorship not stated); Frost 533 requires Malaysia work eligibility; Sattva 62596 requires Kannada; Sattva 62085 asks 5-8 yrs (top of band).
- No undated evergreen consulting reqs found at any firm this week (Avalon and Value Partners only have open-application forms), so none were kept.
