# Tier 3C coverage (sweep date 2026-10-26, window posted_date >= 2026-10-19)

Format: firm | method | postings seen | kept | blocker / notes | back-end ATS evidence beyond apply vendor

- Redseer Strategy Consultants | Zoho Recruit portal https://redseer.zohorecruit.in/jobs/Careers, embedded job JSON + per-job Date_Opened | 5 | 0 | Same 5 ids as last sweep; Associate Consultant opened 2025-10-24, Sector Analyst 2025-09-02, Writer & Editor 2026-08-27, other two older ids. None in window. | Zoho Recruit only.
- Praxis Global Alliance | https://praxisga.hire.trakstar.com/ | 0 | 0 | "No jobs available". | Trakstar Hire.
- Avalon Consulting | https://www.consultavalon.com/work-with-us/apply-now/ | 0 | 0 | General application form only; no listings. | WordPress form.
- Technopak (The Knowledge Company) | https://tkc.in/careers/ + 6 job pages (WP datePublished) | 7 | 0 | Same 7 roles; published 2024-09 to 2026-08 (Marketing Manager 08-21, Digital Marketer 03-11); in-band Senior Associate / Research Associate published 2024-09 / 2025-11. None in window. | WordPress + native form.
- 1Lattice | Trakstar Hire https://1lattice.hire.trakstar.com/?limit=100 (default view shows 25 of 28) + datePosted on each job page | 28 | 0 | 28 openings (2 more than last sweep). In window: Associate Operations B2B (10-23) and B2C (10-19), Manager Network Development (10-16 not in window), Senior Associate/Assistant Manager B2B (10-26): all expert-network ops or team-lead roles, not consulting. | Trakstar Hire.
- Sattva Consulting | Kula https://careers.kula.ai/sattva, RSC payload launch_at + job page | 62 | 1 | Kept: 64141 Associate Consultant Foundations Advisory, implant embedded at Ministry of Skill Development and Entrepreneurship, New Delhi (10-22, 12-month contract, 2-4 yrs, needs prior embedded government experience). Dropped in window: 59120 Senior Consultant People HRBP (10-19, HR). 62596 Kannada implant (10-15) is now before window. | Kula.
- Nexdigm | https://www.nexdigm.com/careers/current-openings/ plain HTTP (all 25 listings are in the DOM, Load More is client-side) | 25 | 0 | Tax, accounting, transfer pricing, CFO services, market-research ops; in-window (relative dates 4-7 days ago): Assistant Manager PMO, Senior Executive CFO, Senior Associate CFO, Team Lead P2P/O2C, Indirect Tax Senior Assistant, Lead Associate AP/GL; none consulting band. | no evidence.
- Tredence | RippleHire POST /candidate/candidatejobsearch (careerSiteUrlParams, token rzuz0vttMaz0VxxVzDiY) + GET candidatejobdetail jobPostingDate for all 55 | 55 | 0 | In window: 918464 Manager Dev Ops AWS & AI (10-26, Hyderabad, 7-12 yrs) and 917272 Senior GCP DevOps & LLMOps Engineer (10-19, Bangalore, engineering). Consulting-title reqs (908545 Consultant Chicago 09-15, 882979, 881317) before window. Firecrawl not used. | RippleHire.
- Fractal Analytics | Workday CXS https://fractal.wd1.myworkdayjobs.com/wday/cxs/fractal/Careers/jobs (117 total) + per-job detail startDate for all postings <=10 days old | 117 | 0 | 12 postings dated 10-19 or later; none qualifies: Principal Consultant CPG London SR-46962 (10-22, Principal, P&L owner), Engagement Manager CPG SR-46963, Senior Business Analyst CPG Amsterdam SR-46929 (10-21, 8+ yrs, 24-month FTC), Senior Associate Mumbai SR-46867 (10-20, Investor Relations), Sr Business Analyst / Senior Decision Scientist Insurance SR-46873 (10-20, New York remote, 5+ yrs analytics), engineering and architect roles. | Workday only.
- Zinnov | Greenhouse boards-api (first_published) | 38 | 0 | In window: Senior Associate Graphic Designer 4438207009 (10-23, design), Engagement Manager M&A 4310352009 (10-22, Manager), 2x Principal Program Management & Consulting (10-19), Associate Director Employer Branding, People Success intern. None in band and consulting. | Greenhouse.
- Everest Group | https://www.everestgrp.com/careers/ + job pages | 5 | 0 | Unchanged: Senior Analyst CIS and Senior Analyst Application Services in band but dated 2026-07-19 / 2025-09-15 (carried from earlier sweep; job pages expose no date meta); 3 Practice Director out of band. | apply via LinkedIn.
- Primus Partners | https://www.primuspartners.in/jobs | 0 | 0 | "0 Results / No jobs found". | no evidence.
- Intellecap | https://www.intellecap.com/current-opportunities | 8 | 0 | All carry 2025 deadlines (Aug 31 / Sep 30 2025); stale. | email apply.
- Wazir Advisors | https://wazir.in/career/ | 1 | 0 | Senior Business Consultant Dubai, 10+ yrs MBA; out of band. | no ATS.
- Analysys Mason | SmartRecruiters public API (releasedDate) + posting detail | 39 | 3 | Kept (all released 10-23): 744000157507184 Associate Consultant Dubai (Arabic or Russian fluency mandatory, graduating by early 2027), 744000157420789 Consultant Strategy & Transaction PE Frankfurt (German required, 3+ yrs Tier 1/2), 744000157455840 Senior Consultant Transaction PE Frankfurt (German required, 4+ yrs). Dropped: none in window besides these. | SmartRecruiters.
- Frost & Sullivan | BambooHR /careers/list + /careers/{id}/detail datePosted for all 57 | 57 | 5 | Kept: 541 Consultant ICT Singapore (10-23, 5-7 yrs), 542 Consultant ICT Petaling Jaya (10-23, 5-7 yrs), 544 Consultant ICT (10-23, 4-6 yrs, location not stated), 546 Associate Growth Advisory (10-23, entry-level, fresh grads), 549 Consultant Industrial (10-26, 4-6 yrs, location not stated). Dropped in window: 543 Senior Consultant CMN (7-8 yrs), 545 Associate Director, 547/548/550/551 VP/SVP. Seniors 534-537 now before window. | BambooHR.
- Value Partners | Firecrawl scrape https://www.valuepartners.com/careers --wait 5000 (1 call via scripts/fc.py) | 0 | 0 | Send-your-CV application forms (management consulting, digital technology); no listings. | no evidence.
- Elixirr | https://elixirr.com/job-openings (31 vacancies, HTML) + Greenhouse API boards/elixirr (16, first_published) | 31 | 0 | Same 31 vacancies; newest first_published 2026-08-10; none in window. | Greenhouse embed.

## Corrected careers URLs (firms.yaml entries that were wrong or moved)
- Praxis Global Alliance: https://praxisga.hire.trakstar.com/
- Avalon Consulting: https://www.consultavalon.com/work-with-us/apply-now/
- Technopak: https://tkc.in/careers/
- Wazir Advisors: https://wazir.in/career/
- Sattva Consulting: https://careers.kula.ai/sattva
- Intellecap: https://www.intellecap.com/current-opportunities
- Elixirr: https://elixirr.com/job-openings (Greenhouse board elixirr)
- Zinnov: Greenhouse board zinnov
- Primus Partners: https://www.primuspartners.in/jobs
- Nexdigm: https://www.nexdigm.com/careers/current-openings/
- Fractal: https://fractal.wd1.myworkdayjobs.com/Careers
- Tredence: https://tredence.ripplehire.com/candidate/?token=rzuz0vttMaz0VxxVzDiY&source=CAREERSITE
- Analysys Mason: https://careers.smartrecruiters.com/AnalysysMason1
- Frost & Sullivan: https://frostsullivan.bamboohr.com/careers
- 1Lattice: https://1lattice.hire.trakstar.com/ (append ?limit=100 to see all openings)
- Redseer: https://redseer.zohorecruit.in/jobs/Careers

## Notes
- Total kept: 9 (Analysys Mason 3, Frost & Sullivan 5, Sattva 1). The prior kept record (Sattva 62596, launched 10-15) falls before the 10-19 window and is dropped.
- Scope coverage (global/uk/india/other) is in tier_3C_scopes.json. Most 3C firms have a single India-centred board and no UK page; recorded as none with reason. Fractal, Analysys Mason, Frost, Elixirr, Zinnov, Tredence are single boards proven via-global with posting ids.
- Firecrawl calls used: 1 (Value Partners). Everything else plain HTTP and public APIs.
- Eligibility flags: Analysys Mason Dubai needs Arabic or Russian; Frankfurt roles need German and English; Sattva 64141 needs prior embedded government experience (12-month contract); Frost 541/542 ask 5-7 yrs (Consultant band, title may be reset after interview); Frost 546 is a fresh-graduate Associate (overqualified); Frost 544/546/549 give no location on the posting.
- Date caveats: Everest and Technopak expose no/old dates; Nexdigm and Wazir only give relative text.
