# Firm registry (draft for review)

Source: `firms/firms.yaml`. ATS and status come from one live request per firm (`firms/probe.json`).
Tracks: A = Digital Strategy & AI, B = Sustainability/ESG.

## Tier 1: MBB (3)

- **McKinsey & Company** | tracks AB | global, india | ATS: unreachable | UNREACHABLE, check URL
  - https://www.mckinsey.com/careers/search-jobs
- **BCG** | tracks AB | global, india | ATS: phenom | ok
  - https://careers.bcg.com/global/en/search-results
- **Bain & Company** | tracks AB | global, india | ATS: unknown | ok, ATS not detected
  - https://www.bain.com/careers/find-a-role/

## Tier 2: Big Four (15)

- **Deloitte (global portal)** | tracks AB | global | ATS: unknown | ok, ATS not detected
  - https://apply.deloitte.com/careers  (landed on https://apply.deloitte.com/en_US/careers)
- **Deloitte USI (India)** | tracks AB | india | ATS: unknown | ok, ATS not detected
  - https://usijobs.deloitte.com/en_US/careersUSI/SearchJobs
- **Deloitte UK** | tracks AB | uk | ATS: avature | ok
  - https://apply.deloitte.co.uk/
- **Deloitte Middle East** | tracks AB | uae, me | ATS: unknown | HTTP 404, check URL
  - https://www2.deloitte.com/xe/en/careers.html  (landed on https://www.deloitte.com/xe/en/careers.html)
- **Monitor Deloitte** | tracks A | global | ATS: unknown | HTTP 404, check URL
  - https://www2.deloitte.com/global/en/pages/strategy-operations/solutions/monitor-deloitte.html  (landed on https://www.deloitte.com/global/en/services/consulting/services/global-strategy-and-operations.html)
- **PwC India** | tracks AB | india | ATS: unknown | bot-blocked, needs Firecrawl/browser
  - https://www.pwc.in/careers.html
- **PwC global** | tracks AB | global | ATS: unknown | bot-blocked, needs Firecrawl/browser
  - https://www.pwc.com/gx/en/careers.html
- **PwC UK** | tracks AB | uk | ATS: unknown | bot-blocked, needs Firecrawl/browser
  - https://www.pwc.co.uk/careers.html
- **PwC Middle East** | tracks AB | uae, me | ATS: unknown | bot-blocked, needs Firecrawl/browser
  - https://www.pwc.com/m1/en/careers.html
- **Strategy& (PwC)** | tracks A | global | ATS: unknown | ok, ATS not detected
  - https://www.strategyand.pwc.com/gx/en/careers.html  (landed on https://www.strategyand.pwc.com/gx/en/join-us.html)
- **EY careers (global)** | tracks AB | global, india | ATS: successfactors | ok
  - https://careers.ey.com
- **EY-Parthenon** | tracks A | global, india | ATS: unknown | HTTP 404, check URL
  - https://www.ey.com/en_gl/careers/ey-parthenon
- **KPMG India** | tracks AB | india | ATS: oracle-hcm | ok
  - https://kpmg.com/in/en/careers.html
- **KPMG global** | tracks AB | global | ATS: unknown | ok, ATS not detected
  - https://kpmg.com/xx/en/careers.html
- **KPMG UK** | tracks AB | uk | ATS: unknown | ok, ATS not detected
  - https://www.kpmgcareers.co.uk/

## Tier 3A: Global strategy firms (15)

- **Kearney** | tracks AB | global, india | ATS: unknown | ok, ATS not detected
  - https://www.kearney.com/careers
- **Oliver Wyman** | tracks AB | global, india | ATS: unreachable | UNREACHABLE, check URL
  - https://careers.oliverwyman.com
- **L.E.K. Consulting** | tracks AB | global, india | ATS: unknown | ok, ATS not detected
  - https://www.lek.com/careers
- **Roland Berger** | tracks AB | global, india | ATS: unknown | ok, ATS not detected
  - https://www.rolandberger.com/en/Careers/  (landed on https://www.rolandberger.com/en/Join/Join-Us/Overview/)
- **Arthur D. Little** | tracks AB | global, india, me | ATS: unknown | ok, ATS not detected
  - https://www.adlittle.com/en/careers
- **Simon-Kucher** | tracks A | global, india | ATS: unknown | ok, ATS not detected
  - https://www.simon-kucher.com/en/careers
- **OC&C Strategy** | tracks A | global, india | ATS: unknown | ok, ATS not detected
  - https://www.occstrategy.com/en/careers  (landed on https://www.occstrategy.com/en/careers/careers-at-occ/)
- **Bridgespan Group** | tracks AB | global, india | ATS: taleo | ok
  - https://www.bridgespan.org/about-us/careers  (landed on https://www.bridgespan.org/careers-at-bridgespan)
- **PA Consulting** | tracks AB | global, uk | ATS: unknown | ok, ATS not detected
  - https://www.paconsulting.com/careers
- **Putnam Associates** | tracks A | global | ATS: greenhouse | ok
  - https://www.putassoc.com/careers  (landed on https://inizio.com/our-businesses/ignite/about-inizio-ignite/our-teams/)
- **Charles River Associates** | tracks A | global | ATS: unknown | ok, ATS not detected
  - https://www.crai.com/careers  (landed on https://www.crai.com/cra-careers/)
- **Sia Partners** | tracks AB | global, india, me | ATS: unknown | ok, ATS not detected
  - https://www.sia-partners.com/en/careers  (landed on https://www.sia-partners.com/en/opportunities)
- **Wavestone** | tracks A | global | ATS: unknown | ok, ATS not detected
  - https://www.wavestone.com/en/careers
- **Dalberg Advisors** | tracks B | global, india | ATS: unknown | HTTP 404, check URL
  - https://dalberg.com/careers
- **FSG** | tracks B | global | ATS: greenhouse | ok
  - https://www.fsg.org/careers  (landed on https://dev-fsg-advisors.pantheonsite.io/about/careers/)

## Tier 3B: Transformation, tech and specialist (incl. ESG) (26)

- **Accenture** | tracks AB | global, india, uk | ATS: workday | ok
  - https://www.accenture.com/in-en/careers/jobsearch
  - note: Consultant tier = 5-10 yrs (gated). Analyst/Sr Analyst tier viable. Use findjobs API; read the body, titles mislead.
- **IBM Consulting** | tracks A | global, india | ATS: unknown | ok, ATS not detected
  - https://www.ibm.com/careers/search
- **Capgemini Invent** | tracks AB | global, india | ATS: unknown | ok, ATS not detected
  - https://www.capgemini.com/careers/join-capgemini/job-search/
- **Infosys Consulting** | tracks A | global, india | ATS: unknown | bot-blocked, needs Firecrawl/browser
  - https://www.infosysconsulting.com/careers  (landed on https://www.infosys.com:443/consulting/)
- **Gartner Consulting** | tracks A | global, india | ATS: unknown | ok, ATS not detected
  - https://jobs.gartner.com
  - note: Req 112692 in flight, see Claude-AI-Coach STATUS.md
- **ZS Associates** | tracks A | global, india | ATS: unknown | ok, ATS not detected
  - https://www.zs.com/careers
- **Alvarez & Marsal** | tracks A | global, india | ATS: unknown | bot-blocked, needs Firecrawl/browser
  - https://www.alvarezandmarsal.com/careers
- **AlixPartners** | tracks A | global | ATS: unknown | ok, ATS not detected
  - https://www.alixpartners.com/careers
- **FTI Consulting** | tracks AB | global, india | ATS: unknown | ok, ATS not detected
  - https://www.fticonsulting.com/careers
- **Berkeley Research Group** | tracks A | global | ATS: workday | ok
  - https://www.thinkbrg.com/careers
- **Grant Thornton** | tracks AB | global, india | ATS: unknown | ok, ATS not detected
  - https://www.grantthornton.in/careers
- **BDO** | tracks AB | global, india | ATS: unknown | ok, ATS not detected
  - https://www.bdo.global/en-gb/careers  (landed on https://www.bdo.global/en-gb/microsites/bdo-pvp/working-at-bdo)
- **Protiviti** | tracks A | global, india | ATS: unknown | ok, ATS not detected
  - https://www.protiviti.com/in-en/careers
- **Mercer** | tracks A | global, india | ATS: phenom | ok
  - https://www.mercer.com/en-in/careers/  (landed on https://careers.marsh.com/global/en/people-and-investments)
- **WTW (Willis Towers Watson)** | tracks A | global, india | ATS: unknown | bot-blocked, needs Firecrawl/browser
  - https://www.wtwco.com/en-in/careers
- **Guidehouse** | tracks AB | global | ATS: workday | ok
  - https://guidehouse.com/careers
- **ICF** | tracks B | global, india | ATS: phenom | ok
  - https://www.icf.com/careers  (landed on https://careers.icf.com/us/en)
- **ERM** | tracks B | global, india | ATS: workday | ok
  - https://www.erm.com/careers/  (landed on https://www.erm.com/erm-careers/)
- **Ramboll** | tracks B | global, india | ATS: smartrecruiters | ok
  - https://ramboll.com/careers  (landed on https://www.ramboll.com/careers)
- **WSP** | tracks B | global, india | ATS: unknown | bot-blocked, needs Firecrawl/browser
  - https://www.wsp.com/en-in/careers  (landed on https://www.wsp.com/en-gl/sites/india)
- **Arup** | tracks B | global, india | ATS: unknown | ok, ATS not detected
  - https://www.arup.com/careers
- **Anthesis** | tracks B | global | ATS: unknown | ok, ATS not detected
  - https://www.anthesisgroup.com/careers
- **South Pole** | tracks B | global, india | ATS: unknown | bot-blocked, needs Firecrawl/browser
  - https://www.southpole.com/careers
- **Carbon Trust** | tracks B | global, uk | ATS: unknown | ok, ATS not detected
  - https://www.carbontrust.com/about-us/careers  (landed on https://www.carbontrust.com/who-we-are/our-career-opportunities)
- **Slalom** | tracks A | global | ATS: unknown | ok, ATS not detected
  - https://www.slalom.com/us/en/careers
- **Huron Consulting** | tracks A | global, india | ATS: workday | ok
  - https://www.huronconsultinggroup.com/careers  (landed on https://www.huronconsultinggroup.com/en-in/careers)

## Tier 3C: Boutiques and regional (18)

- **Redseer Strategy Consultants** | tracks A | india, me | ATS: unknown | ok, ATS not detected
  - https://redseer.com/careers/
- **Praxis Global Alliance** | tracks A | india, global | ATS: unknown | HTTP 404, check URL
  - https://www.praxisga.com/careers
- **Avalon Consulting** | tracks A | india | ATS: unreachable | UNREACHABLE, check URL
  - https://www.avalonconsulting.com/careers
- **Technopak** | tracks A | india | ATS: unknown | HTTP 404, check URL
  - https://www.technopak.com/careers
- **1Lattice** | tracks A | india | ATS: unknown | ok, ATS not detected
  - https://1lattice.com/careers  (landed on https://www.1lattice.com/careers)
- **Sattva Consulting** | tracks B | india | ATS: unknown | ok, ATS not detected
  - https://www.sattva.co.in/careers  (landed on https://www.sattva.co.in/join-us/careers/)
- **Nexdigm** | tracks AB | india | ATS: unknown | ok, ATS not detected
  - https://nexdigm.com/careers  (landed on https://www.nexdigm.com/careers/)
- **Tredence** | tracks A | india, global | ATS: unknown | ok, ATS not detected
  - https://www.tredence.com/careers  (landed on https://www.tredence.com/careers/greatest-of-ai)
- **Fractal Analytics** | tracks A | india, global | ATS: workday | ok
  - https://fractal.ai/careers  (landed on https://fractal.wd1.myworkdayjobs.com/Careers)
- **Zinnov** | tracks A | india | ATS: unknown | ok, ATS not detected
  - https://zinnov.com/careers
- **Everest Group** | tracks A | india, global | ATS: unknown | ok, ATS not detected
  - https://www.everestgrp.com/careers
- **Primus Partners** | tracks AB | india | ATS: unknown | ok, ATS not detected
  - https://www.primuspartners.in/careers
- **Intellecap** | tracks B | india | ATS: unknown | ok, ATS not detected
  - https://www.intellecap.com/careers
- **Wazir Advisors** | tracks A | india | ATS: unknown | HTTP 404, check URL
  - https://www.wazir.in/careers  (landed on https://wazir.in/careers)
- **Analysys Mason** | tracks A | global, me, india | ATS: smartrecruiters | ok
  - https://www.analysysmason.com/careers/
- **Frost & Sullivan** | tracks A | global, india, me | ATS: unknown | ok, ATS not detected
  - https://www.frost.com/careers/
- **Value Partners** | tracks A | global, me | ATS: unknown | ok, ATS not detected (JS shell?)
  - https://www.valuepartners.com/careers
- **Elixirr** | tracks A | global, uk | ATS: unknown | ok, ATS not detected
  - https://elixirr.com/careers  (landed on https://www.elixirr.com/en-gb/careers/)

## Probe summary

- 77 firms, 17 clean, 9 bot-blocked, 19 need URL fixes, 57 with no ATS detected.