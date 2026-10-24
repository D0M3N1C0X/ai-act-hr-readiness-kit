# Method

How the register classifies a system, decides what it owes and whom to tell, and the choices the text leaves open.
Sources and their status are in [verification.md](verification.md).

## The answers about each system

Every system has the same eighteen answers in [`data/ai_systems.csv`](../data/ai_systems.csv), with a written
rationale. They are inputs in the workbook's Register sheet, so a reviewer who disagrees with one changes it and sees
the consequences.

| Answer | Values | Used for |
|---|---|---|
| Used in IT / PL / DE / ES; department in scope | Yes/No; a department or All | workers in scope; which national rules |
| Used on applicants | Yes/No | whether the system reaches workers or only candidates |
| Infers emotions; for medical or safety reasons | Yes/No | Art. 5(1)(f) |
| Annex III point 4 | None, 4(a), 4(b) | Art. 6(2) |
| Profiles people; Art. 6(3) condition | Yes/No; None, (a)-(d) | Art. 6(3) |
| Talks to people | Yes/No | Art. 50(1) |
| Decides or helps decide about people | Yes/No | Art. 26(11), Art. 86 |
| Fully automated; monitors workers | Yes/No | Italy art. 1-bis, Statuto art. 4, Kodeks pracy art. 22³ |
| Employer controls the input data | Yes/No | Art. 26(4) |
| Supplier | Vendor, In-house | Art. 3(3) and (11): who is the provider |
| Type and model on the market before 2 December 2027 | Yes/No | Art. 111(2): when the high-risk duties bite |

## Classification, in order

1. **Prohibited** - infers emotions and is not for medical or safety reasons (Art. 5(1)(f)).
2. **High-risk** - in Annex III point 4 and profiling people; or in Annex III with no Art. 6(3) condition.
3. **Not high-risk (Art. 6(3))** - in Annex III, no profiling, and one of the four conditions met.
4. **Transparency only** - outside Annex III and talks to people (Art. 50(1)).
5. **Minimal risk** - everything else.

The order matters: a prohibited practice is prohibited even if it would also be high-risk, and profiling closes the
Art. 6(3) door whatever the condition claimed.

## Obligations

Thirteen obligations, each with the condition that triggers it and the date it applies from
(`OBLIGATIONS` in [`src/config.py`](../src/config.py)). The choices:

- **AI literacy applies to every system in use**, including minimal-risk ones: Art. 4 is about staff, not about risk.
- **Informing workers under Art. 26(7)** is counted for high-risk systems used on employees; for recruitment
  systems the people affected are applicants, who are told under Art. 26(11).
- **The right to an explanation (Art. 86)** is dated with the high-risk duties. Article 86 sits in a chapter that
  applies from 2 August 2026, but it attaches to decisions based on high-risk Annex III systems, a classification in
  Chapter III that applies to them from 2 December 2027.
- **The in-house attrition model** carries the provider's duties (Art. 16) because the employer puts it into service
  for its own use (Art. 3(3) and (11)); the register does not list the provider's duties one by one.
- **Systems already on the market (Art. 111(2), as amended by Reg. 2026/1744).** A high-risk system whose type and
  model was on the market or in service before 2 December 2027 falls under the Regulation only once its design
  changes significantly; recital 39 makes the type and model, not the employer's installation, decisive. The register
  shows this in a column of its own and keeps the obligations listed, because a supplier's next major release or a
  retrained in-house model ends the grace period.
- **Annex III point 3** (education and vocational training) is ruled out for the learning recommendations: it covers
  training institutions, and the courses suggested do not feed promotion or pay.

## Telling the workers

Eight national rules (`WORKER_RULES`), each tied to the answers:

| Rule | Triggered when the system is used in the country and |
|---|---|
| IT art. 1-bis | used on employees, fully automated, and high-risk or monitoring workers (applicants who are hired are told at hiring) |
| IT Statuto art. 4 | monitors workers |
| DE §90 and §80(3) | used in Germany at all: every system changes how HR staff or others work |
| DE §87(1) Nr. 6 | monitors workers, or is used on employees and high-risk; a minimum, since courts read "able to monitor" broadly |
| DE §95 | Annex III 4(a), profiling and deciding about people: it applies selection criteria (§95(1); §95(2a) where AI helps draw them up) |
| ES art. 64.4.d | high-risk: it affects decisions on working conditions or access to employment |
| PL art. 22³ | monitors workers |

A prohibited system triggers none of them: it has to stop, not be notified.

## Two engines, one answer

`src/register.py` computes the class, the role, the workers in scope and every obligation and rule; the workbook
recomputes all of them with live formulas written as the same tests in the same order, and its Reconciliation sheet
checks every pair. CI recalculates the workbook with LibreOffice; the tests calculate it in pure Python with
[excel-twin](https://github.com/D0M3N1C0X/excel-twin), and check that changing an answer reclassifies a system in
the workbook. Answers must be spelled exactly as allowed (`register.validate`): Excel compares text without regard to
case and Python does not, so a stray "yes" would let them disagree. The browser tool's `web/engine.js` is checked
against Python on the twelve systems and 2,000 random ones.
