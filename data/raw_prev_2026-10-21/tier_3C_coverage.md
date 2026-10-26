# Tier 3C coverage (sweep date 2026-10-21, window posted_date >= 2026-10-14)

Format: firm | method | postings seen | kept | blocker / notes | back-end ATS evidence beyond apply vendor

- Redseer Strategy Consultants | Zoho Recruit portal https://redseer.zohorecruit.in/jobs/Careers, embedded job JSON | 5 | 0 | Same 5 listing ids as last sweep (Associate Consultant, Sector Analyst, Writer & Editor Sr Associate, Senior Consultant, Sector Lead); none newer, all dated before window last sweep. | Zoho Recruit only.
- Praxis Global Alliance | https://praxisga.hire.trakstar.com/ | 0 | 0 | "No jobs available". | Trakstar Hire.
- Avalon Consulting | https://www.consultavalon.com/work-with-us/apply-now/ | 0 | 0 | General application form only; no listings. | WordPress form.
- Technopak (The Knowledge Company) | https://tkc.in/careers/ | 7 | 0 | Same 7 roles as last sweep, in-band ones dated 2024-2025. | WordPress + native form.
- 1Lattice | Trakstar Hire https://1lattice.hire.trakstar.com/ | 26 | 0 | 26 openings (2 more than last sweep) but all Account Manager BD / Assistant Manager / Associate Director / Manager / Director / PM / CA / design / PR / ops; no Analyst-Consultant band. No dates. | Trakstar Hire.
- Sattva Consulting | Kula https://careers.kula.ai/sattva, RSC payload with launch_at | 62 | 1 | Kept: Associate Consultant CSR Bengaluru implant (62596, 10-15, 2-4 yrs, Kannada mandatory). Dropped in window: 62250 Consultant Business & Financial Operations (10-14, internal finance), 62675 Engagement Manager Government Advisory (10-15, Manager), 59120 Senior Consultant People HRBP (10-19, HR). Roles dated 10-09 to 10-11 from last sweep are now before window. | Kula.
- Nexdigm | https://www.nexdigm.com/careers/current-openings/ via Playwright, Load More exhausted | 20 | 0 | Tax, accounting, transfer pricing, market-research ops, trainee roles; no consulting-band role; no dates. | no evidence.
- Tredence | RippleHire POST /candidate/candidatejobsearch (token rzuz0vttMaz0VxxVzDiY) | 57 | 0 | Same 57 reqs, newest 915218 unchanged; no dates exposed; no new band-title role. Firecrawl not used. | RippleHire.
- Fractal Analytics | Workday CXS https://fractal.wd1.myworkdayjobs.com/wday/cxs/fractal/Careers/jobs (119 total) + per-job detail startDate | 119 | 0 | 16 postings dated 10-12 onward; none qualifies: Senior Consultant Pharma SR-46513 (10-16, NY, 6+ yrs, no sponsorship), Senior Decision Scientist SR-44857 (10-16, London, 4-5+ yrs, no visa sponsorship, data science), Senior Associate SR-46867 (Investor Relations). Senior Consultant Marketing Analytics SR-46751 (kept last sweep) is dated 10-13, now before window. | Workday only.
- Zinnov | Greenhouse boards-api (first_published) | 36 | 0 | In window: 2 x Principal - Program Management & Consulting (10-19, Bangalore), Principal band, dropped. | Greenhouse.
- Everest Group | https://www.everestgrp.com/careers/ + job pages | 5 | 0 | Unchanged: Senior Analyst CIS and Senior Analyst Application Services in band but published 2026-07-19 / 2025-09-15 (last sweep); 3 Practice Director out of band. Job pages no longer expose date meta, WP REST route not available; dates carried from last sweep (published dates are immutable). | apply via LinkedIn.
- Primus Partners | https://www.primuspartners.in/jobs | 0 | 0 | "0 Results / No jobs found". | no evidence.
- Intellecap | https://www.intellecap.com/current-opportunities | 8 | 0 | All 8 carry 2025 deadlines; stale. | email apply.
- Wazir Advisors | https://wazir.in/career/ (browser UA) | 1 | 0 | Senior Business Consultant Dubai, 10+ yrs MBA; out of band. | no ATS.
- Analysys Mason | SmartRecruiters public API (releasedDate) | 39 | 0 | No posting released on or after 10-14 (latest 10-08). | SmartRecruiters.
- Frost & Sullivan | BambooHR /careers/list + /careers/{id}/detail datePosted | 51 | 0 | In window: VP Revenue Operations x2 (534, 535), Executive Sales Support (537), Senior Consultant Growth Strategy Riyadh (536, 6+ yrs, 2 yrs Gulf). Research Analyst Cybersecurity 533 (kept last sweep) is dated 10-13, now before window. | BambooHR.
- Value Partners | https://www.valuepartners.com/careers | 0 | 0 | Send-your-CV CTAs only (Milan/Turin); no listings. | no evidence.
- Elixirr | https://elixirr.com/job-openings via Playwright (31) + Greenhouse API boards/elixirr (16, first_published) | 31 | 0 | Same 31 vacancies; no in-band role first published on/after 10-14 (newest 2027 Graduate Analyst 08-06). | Greenhouse embed.

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
- 1Lattice: https://1lattice.hire.trakstar.com/
- Redseer: https://redseer.zohorecruit.in/jobs/Careers

## Notes
- Total kept: 1 (Sattva 62596), carried unchanged from the 10-15 record (launch_at 10-15 is inside the window).
- Scope coverage (global/uk/india/other) is in tier_3C_scopes.json. Most 3C firms have a single India-centred board and no UK page; recorded as none with reason. Fractal, Analysys Mason, Frost, Elixirr, Zinnov, Tredence are single boards proven via-global with posting ids.
- Firecrawl calls used: 0. Plain HTTP, public APIs, Playwright (Elixirr, Nexdigm).
- Eligibility flags: Sattva 62596 requires Kannada.
