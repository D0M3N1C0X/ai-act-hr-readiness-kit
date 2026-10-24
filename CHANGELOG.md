# Changelog

What changed in each release. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
