# Changelog

What changed in each release. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- **The classification put to the test** (report section 8, `src/guideline_cases.py`, `data/guideline_cases.csv`):
  the 21 workplace cases of emotion recognition in the Commission's guidelines on prohibited practices (C(2025) 5052
  final, 29 July 2025), each with its paragraph and verdict. Read literally, the kit's first questions agreed on 13:
  they would have banned emotion read from written text, from customers and for the worker's own training, and
  allowed wellbeing, stress, burnout and property monitoring. And a fragility check: the interview scheduler is the one
  class that rests on three answers.

- **The in-house model as a real case** (report section 9, `src/provider_file.py`, `data/provider_file_s07.csv`): the
  attrition model built in hr-people-analytics set against the 21 provider duties of Articles 9 to 20, 43, 47 to 49,
  72 and 73: 3 covered, 10 partly, 8 missing. Its model card is vendored with a pinned checksum, and a test checks it
  states the register's class and role and answers all 14 supplier questions the register would send.

- **The pay review recommender under both laws** (report section 10, `src/pay_review.py`): four designs, one 3%
  budget, run on the pay transparency kit's payroll (vendored, its figures reproduced before any rise). Rating only,
  the merit matrix and a retention boost move the group gap by at most 0.1 points; an equity fund of €1.91 million,
  the kit's cost ceiling, clears all 12 flags and brings the gap to 15.5%. The retention boost is the use the
  attrition model's card rules out.

- **Who supervises, country by country** (report section 11, `data/national_authorities.csv`): the AI Act
  authorities and national AI acts for the nine countries, read in the original where this environment could reach
  it. Verified: Poland (Dz.U. 2026 poz. 1003), Germany (KI-MIG, BGBl. 2026 I Nr. 223), Ireland (S.I. 366/2025 and
  405/2026: the Workplace Relations Commission supervises HR systems); Spain's AESIA statute. Italy's Law 132/2025
  is from secondary sources and marked to verify; the Netherlands has a draft; France, Austria and Belgium were not
  checked.

- **Two workbook sheets**: *Guideline cases* (the 21 cases' facts as inputs; the answers, the verdict and the
  agreement as formulas) and *Provider file* (the 21 provider duties with a status drop-down and live counts).
  Reconciliation checks: 813 → 838, all matching after a LibreOffice recalculation. New cover and tool loop.

### Fixed

- **The emotion and medical-or-safety questions**, in the register, the workbook and the browser tool, now follow the
  guidelines: emotions of workers or candidates from biometric data; a medical use or a specific danger to life and
  health only. Verification register: A02 verified, A20-A24 added.

## [1.2.0] - 2026-11-06

### Added

- **Five more countries**: France (the CSE under L2312-38 and L2312-8, and each candidate and employee under L1221-8
  to L1222-4), the Netherlands (works council advice under art. 25(1)(k) WOR and consent under art. 27(1)), Ireland
  (the information and consultation forum of the 2006 Act), Austria (ArbVG §91(2), §96a and §96(1) Z 3) and Belgium
  (CCT n° 39 and n° 81): eleven rules, nineteen in all, in the three engines, the tool and the worker information
  pack, each read in an official source.
- **Who the deployer is**: private employer, public body, or private entity providing public services, in the
  workbook's Settings and as a choice in the tool. It decides two new obligations, the fundamental rights impact
  assessment (O14, Art. 27) and registering the use (O15, Art. 26(8), 49(3)), and the 2 August 2030 long stop for a
  public body's systems already on the market (Art. 111(2)).
- **Questions for the supplier**: sixteen questions, each tied to the duty it serves (Art. 13(3), 26, 50, 6(4),
  111(2) and the national notices), asked of each bought system as its answers require; a `Supplier` sheet and
  `deliverables/supplier_questionnaire.md`.
- **AI literacy plan**: six modules for named groups of people, triggered by each system's answers, under Article 4
  as replaced by the Omnibus; a `Literacy` sheet and `deliverables/ai_literacy_plan.md`.
- **Fundamental rights impact assessment**: when it is owed, its six elements mapped to the GDPR Article 35(7) DPIA
  now that Article 27(4) allows cross-references, and a draft for each high-risk system in
  `deliverables/fria_drafts.md`, voluntary for a private employer.
- Reconciliation grows from 330 to 813 checks; the browser engine is checked on 16,309 values, the twelve systems
  under each kind of deployer included.

### Changed

- The verification register gains an "Official copy" status and records what was read through official open-data
  services because EUR-Lex, Légifrance and the RIS refuse automated reads.

## [1.1.0] - 2026-10-24

### Added

- **[Browser tool](https://d0m3n1c0x.github.io/ai-act-hr-readiness-kit/tool/)**: guided questions or a list in Excel or
  CSV; class and reason, obligations with dates, national rules, Excel download; English and Italian; nothing leaves
  the computer. `web/engine.js` is checked against Python on 12,090 values.
- **Article 111(2), as amended by Regulation (EU) 2026/1744**: a high-risk system whose type and model was on the
  market before 2 December 2027 falls under the duties only at its next significant design change. A new answer and a
  column in the register say when each system's duties bite.
- Answers are validated: Excel compares text without regard to case and Python does not.

### Fixed

After an independent legal and code review:

- A system that profiles people but also names an Article 6(3) condition is high-risk; the national rules that follow
  the class now follow it too, in all three engines.
- The employer is the provider of its in-house model under Article 3(3) and (11), not Article 25.
- Article 50(1) is presented as the supplier's duty, which the employer checks.
- Italy: art. 1-bis informs workers, so applicant-only systems are left out; the 24-hour rule is co. 5; the model
  notice now covers every item of co. 2, the right of access (co. 3) and the format (co. 6); Statuto art. 4 read and
  stated with its purposes and exemptions.
- Germany: §90 and §80(3) apply to every system used in Munich; §87(1) Nr. 6 is a minimum; §95(1) is the basis for
  selection criteria; the §80(3) expert is agreed with the employer.
- Spain: "before use" labelled as the prudent reading of art. 64.4.d. Poland: art. 22³ §4 and its purpose limit.
- The reconciliation summary counts matches, so a check that turns into an error is reported as a failure.

## [1.0.0] - 2026-10-24

First release: twelve HR AI systems classified, thirteen obligations, eight national rules, an Excel register
reconciled with Python, a report and a worker information pack.
