# AI Act readiness for HR: what the employer must do, by when, and whom to tell

**Scope:** the 12 AI systems the HR function uses at an employer in Italy, Poland, Germany and Spain, with 3,443 workers
**Method:** each system classified from the answers in the register, in Python and in a live Excel model, reconciled cell by cell
**Law:** Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744, both read in the Official Journal; national rules on informing and consulting workers in the four countries

> A dry run, not legal advice. The organisation is the one in [pay-transparency-readiness-kit](https://github.com/D0M3N1C0X/pay-transparency-readiness-kit); its AI systems are invented to cover the cases an HR function meets. Boundary cases are named as such.

## The answer

- **One system has to stop now.** The video interview analysis pilot in Barcelona infers candidates' emotions from their voice and face. Inferring emotions in the workplace has been prohibited since 2 February 2025 unless it is for medical or safety reasons (Art. 5(1)(f)); the fine reaches €35 million or 7% of worldwide turnover (Art. 99(3)).
- **Seven systems are high-risk**: CV screening and ranking, targeted job advertising, customer service performance analytics, shift scheduling optimiser, attrition-risk model, pay review recommender, internal mobility matching. Their duties start on 2 December 2027, 404 days from this assessment: the Digital Omnibus moved them from 2 August 2026.
- **The attrition-risk model makes the employer a provider.** HR analytics built it, so the employer carries the provider's duties for it as well as the user's: quality management, technical documentation, conformity assessment and registration (Art. 16 and 25). It is the heaviest single item in the register.
- **Two duties already apply.** AI literacy for the staff who use 11 systems (Art. 4, since February 2025, now worded as measures to take rather than a level to guarantee), and telling people they are talking to an AI for 2 systems (Art. 50(1), since August 2026).
- **Telling the workers is already national law, whatever the AI Act's timetable.** In Germany the works council has to be informed about 8 systems and agree to 5 before they are used; in Spain it is owed the parameters of 7; in Italy 2 fully automated systems must be disclosed to the people they affect and to the unions, and 1 monitoring tool needs a union agreement; in Poland 1 monitoring tool needs two weeks' notice.

## 1. The register

| System | HR function | Class | Role | Workers in scope |
|---|---|---|---|---|
| CV screening and ranking | Recruitment | High-risk | Deployer | 3,443 |
| Targeted job advertising | Recruitment | High-risk | Deployer | 3,443 |
| Video interview analysis | Recruitment | Prohibited | Deployer | 493 |
| Interview scheduling assistant | Recruitment | Not high-risk (Art. 6(3)) | Deployer | 3,443 |
| Customer service performance analytics | Performance | High-risk | Deployer | 996 |
| Shift scheduling optimiser | Workforce planning | High-risk | Deployer | 851 |
| Attrition-risk model | Retention | High-risk | Provider and deployer | 3,443 |
| Pay review recommender | Reward | High-risk | Deployer | 3,443 |
| HR service chatbot | HR service | Transparency only | Deployer | 3,443 |
| Learning recommendations | Learning | Minimal risk | Deployer | 3,443 |
| Writing and translation assistant | HR service | Minimal risk | Deployer | 282 |
| Internal mobility matching | Talent | High-risk | Deployer | 3,443 |

*Workers in scope: employees of the employers and departments where the system is used. Recruitment systems also reach applicants, who are not counted.*

How the class is decided, in this order:

1. **Prohibited** if the system infers emotions at work and is not there for medical or safety reasons (Art. 5(1)(f)).
2. **High-risk** if it is used for recruitment or selection (Annex III 4(a)), or for decisions on terms of work, promotion, termination, task allocation, or monitoring and evaluating people (4(b)), unless one of the four conditions of Art. 6(3) applies; a system that profiles people is high-risk in every case.
3. **Not high-risk under Art. 6(3)** if it is in Annex III but only performs a narrow procedural or preparatory task, or improves or checks a human decision, without profiling. The provider documents why.
4. **Transparency only** if it talks to people (Art. 50(1)); otherwise **minimal risk**, with AI literacy as the one duty.

## 2. What applies, and when

| Obligation | Article | From | Systems | Status |
|---|---|---:|---:|---|
| AI literacy of the staff who operate or use it | Art. 4 | 2 February 2025 | 11 | In force |
| Stop the prohibited use | Art. 5(1)(f) | 2 February 2025 | 1 | In force |
| People told they are talking to an AI | Art. 50(1) | 2 August 2026 | 2 | In force |
| Use as instructed, with named human oversight | Art. 26(1)-(2) | 2 December 2027 | 7 | Ahead |
| Input data relevant and representative | Art. 26(4) | 2 December 2027 | 7 | Ahead |
| Monitor; report risks and serious incidents; suspend | Art. 26(5) | 2 December 2027 | 7 | Ahead |
| Keep the logs for at least six months | Art. 26(6) | 2 December 2027 | 7 | Ahead |
| Tell workers' representatives and affected workers before use | Art. 26(7) | 2 December 2027 | 5 | Ahead |
| Data protection impact assessment built on the provider's information | Art. 26(9); GDPR Art. 35 | 2 December 2027 | 7 | Ahead |
| Tell the people decisions are made about | Art. 26(11) | 2 December 2027 | 6 | Ahead |
| Explain a decision on request | Art. 86 | 2 December 2027 | 6 | Ahead |
| Provider duties for a system built in-house | Art. 16 and 25 | 2 December 2027 | 1 | Ahead |
| Not-high-risk assessment documented | Art. 6(4) | 2 December 2027 | 1 | Ahead |

Considered and not applicable:

- **Fundamental rights impact assessment** (Art. 27). Owed by public bodies, private entities providing public services, and deployers of credit and insurance systems (Annex III 5(b)-(c)). A private employer using HR systems is none of these.
- **Registration of the use in the EU database** (Art. 26(8), 49(3)). Owed by deployers that are public authorities. A provider registers its own systems (Art. 49(1)), which here means the in-house attrition model.

## 3. Telling the workers, country by country

The AI Act adds its own duty for high-risk systems from December 2027: inform workers' representatives and the affected workers before use (Art. 26(7)), for 5 systems here. The national rules below apply now, and they reach further than the AI Act's high-risk list.

**IT · Milan**

- **Information on automated decision or monitoring systems** (D.lgs. 152/1997 art. 1-bis; L. 132/2025 art. 11): Targeted job advertising, Shift scheduling optimiser. Purposes, logic, data and parameters, controls, accuracy and possible discriminatory effects, in writing to each worker and to the union representatives (RSA/RSU); before work starts, or 24 hours before a change.
- **Agreement or authorisation for tools that can monitor workers** (Statuto dei lavoratori, art. 4): Customer service performance analytics. An agreement with the union representatives or, failing that, authorisation by the labour inspectorate; before the tool is installed.

**PL · Kraków**

- **Notice of monitoring other than video** (Kodeks pracy art. 22³): Customer service performance analytics. Purpose, scope and method in the workplace rules; notice to each worker; at least two weeks before it starts.

**DE · Munich**

- **Information and consultation on planned AI in work procedures** (BetrVG §90(1) Nr. 3, §90(2)): Customer service performance analytics, Shift scheduling optimiser, Attrition-risk model, Pay review recommender, HR service chatbot, Learning recommendations, Writing and translation assistant, Internal mobility matching. Inform the works council with the documents, and consult it while its views can still change the plan; at the planning stage.
- **Co-determination on technical devices able to monitor conduct or performance** (BetrVG §87(1) Nr. 6): Customer service performance analytics, Shift scheduling optimiser, Attrition-risk model, Pay review recommender, Internal mobility matching. A works agreement; without it the system cannot lawfully be used; before introduction.
- **Co-determination on selection guidelines, also when AI is used** (BetrVG §95(1), (2a)): CV screening and ranking, Targeted job advertising, Internal mobility matching. Works council consent to the selection criteria; before use in hiring, transfer or dismissal decisions.
- **An expert for the works council, deemed necessary for AI** (BetrVG §80(3)): Customer service performance analytics, Shift scheduling optimiser, Attrition-risk model, Pay review recommender, HR service chatbot, Learning recommendations, Writing and translation assistant, Internal mobility matching. Budget and access for an expert of the works council's choosing; when the works council assesses the system.

**ES · Barcelona**

- **Information on the parameters of algorithms affecting work** (Estatuto de los Trabajadores art. 64.4.d): CV screening and ranking, Targeted job advertising, Customer service performance analytics, Shift scheduling optimiser, Attrition-risk model, Pay review recommender, Internal mobility matching. The parameters, rules and instructions the system is based on, to the works council; before use, and with the periodicity that applies.

The [worker information pack](../docs/worker-information.md) has, for each country, who to tell, what the notice must contain and a model text.

## 4. The judgement calls

- **Shift scheduling is a boundary case.** On availability and certified skills alone it might not evaluate anyone; past attendance makes it allocate tasks on individual behaviour, which is profiling. The register classifies it as high-risk, and a supplier that drops attendance from the inputs would change the answer.
- **The interview scheduler is not high-risk, on the provider's word.** It performs a narrow procedural task (Art. 6(3)(a)), but the documented assessment is the provider's to make (Art. 6(4)); the employer should hold a copy, and revisit it if the tool starts ranking candidates.
- **The pay review recommender sits under two laws.** It is high-risk under the AI Act (Annex III 4(b)), and its criteria must be objective and gender-neutral under the Pay Transparency Directive (Art. 4), whose categories and 5% screen are in [pay-transparency-readiness-kit](https://github.com/D0M3N1C0X/pay-transparency-readiness-kit).
- **Learning recommendations stay minimal only while they do not count.** If course completion fed promotion or pay, the system would move into Annex III 4(b).
- **The right to an explanation (Art. 86)** is in a chapter that applies from August 2026, but it attaches to decisions based on high-risk Annex III systems, a classification that applies from December 2027. The register dates it with the high-risk duties; the reading should be confirmed.
- **Data protection law does not wait for 2027.** A data protection impact assessment is already owed for high-risk processing of employees' data (GDPR Art. 35); from December 2027 the AI Act adds that it must use the provider's information (Art. 26(9)). For the two fully automated systems, GDPR Art. 22 already limits decisions based solely on automated processing.
- **Germany's co-determination is the binding constraint now.** A system able to monitor conduct or performance needs a works agreement before it is introduced (BetrVG §87(1) Nr. 6); five systems here already process performance data of workers in Munich.

## 5. The next 90 days

1. **Stop the video interview analysis pilot** in Barcelona, delete the scores, and tell the supplier and the candidates assessed.
2. **Decide the attrition-risk model's future**: keep it and build the provider's file, buy a supplier's equivalent, or narrow it to a team-level view that profiles no one.
3. **Open the works council agenda in Munich** with the information and co-determination items, and send the Spanish works council the parameters of the systems that affect work.
4. **Send the Italian notices** for the fully automated systems and settle the agreement for the monitoring tool; give the Polish notice two weeks before any new monitoring.
5. **Put AI literacy on record**: who uses which system, what training they had, what they still need.
6. **Ask each supplier of a high-risk system** for the instructions for use and the information needed for the data protection impact assessments, and name an overseer per system.

## 6. Method, sources and limits

- **Two engines, one answer.** Every class, role and obligation is computed in Python and again by live formulas in [the register workbook](../deliverables/ai_act_hr_register.xlsx); its Reconciliation sheet checks each pair, and CI recalculates the workbook with LibreOffice.
- **Law read in the original.** The AI Act and the Digital Omnibus in the Official Journal; the national rules on the official legal databases, each with its status in [docs/verification.md](../docs/verification.md).
- **Limits.** Invented systems and answers; the classification follows the text of the Regulation, and Commission guidelines, harmonised standards or national practice can move boundary cases. Not legal advice.

