# AI Act readiness for HR: what the employer must do, by when, and whom to tell

**Scope:** the 12 AI systems the HR function uses at an employer in Italy, Poland, Germany and Spain, with 3,443 workers
**Method:** each system classified from the answers in the register, in Python and in a live Excel model, reconciled cell by cell
**Law:** Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744, both read in the Official Journal; national rules on informing and consulting workers in nine countries: the employer's four, and France, the Netherlands, Ireland, Austria and Belgium for anyone running the tool

> A dry run, not legal advice. The organisation is the one in [pay-transparency-readiness-kit](https://github.com/D0M3N1C0X/pay-transparency-readiness-kit); its AI systems are invented to cover the cases an HR function meets. Boundary cases are named as such.

## The answer

- **One system has to stop now.** The video interview analysis pilot in Barcelona infers candidates' emotions from their voice and face. Inferring emotions in the workplace has been prohibited since 2 February 2025 unless it is for medical or safety reasons (Art. 5(1)(f)); the fine reaches €35 million or 7% of worldwide turnover (Art. 99(3)).
- **Seven systems are high-risk**: CV screening and ranking, targeted job advertising, customer service performance analytics, shift scheduling optimiser, attrition-risk model, pay review recommender, internal mobility matching. The high-risk duties apply from 2 December 2027, 404 days from this assessment, after the Digital Omnibus moved them from 2 August 2026. A system whose type and model was already on the market by then falls under them only when its design changes significantly (Art. 111(2), as amended); all seven are in that position. Cloud HR software changes often, so the safe plan is December 2027.
- **The attrition-risk model makes the employer a provider.** HR analytics put it into service for the employer's own use, so the employer carries the provider's duties as well as the user's: quality management, technical documentation, conformity assessment and registration (Art. 3(3) and 16). It is the heaviest single item in the register.
- **One duty already applies to every system in use.** AI literacy for the staff who use 11 systems (Art. 4, since February 2025, now worded as measures to take rather than a level to guarantee). Telling people they are talking to an AI is the supplier's duty for 2 systems (Art. 50(1), since August 2026); the employer checks it is switched on.
- **Telling the workers is already national law, whatever the AI Act's timetable.** In Germany the works council has to be informed about 11 systems and agree to at least 5 before they are used; in Spain it is owed the parameters of 7; in Italy 1 fully automated system needs a written notice to each worker and the unions, and 1 monitoring tool needs a union agreement; in Poland 1 monitoring tool needs two weeks' notice.

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

*Workers in scope: employees of the employers and departments where the system is used. Recruitment systems also reach applicants, who are not counted. The same register runs on any list of systems in the [browser tool](https://d0m3n1c0x.github.io/ai-act-hr-readiness-kit/tool/).*

How the class is decided, in this order:

1. **Prohibited** if the system infers emotions at work and is not there for medical or safety reasons (Art. 5(1)(f)).
2. **High-risk** if it is used for recruitment or selection (Annex III 4(a)), or for decisions on terms of work, promotion, termination, allocating tasks based on individual behaviour or personal traits, or monitoring and evaluating people (4(b)), unless one of the four conditions of Art. 6(3) applies; a system that profiles people is high-risk in every case.
3. **Not high-risk under Art. 6(3)** if it is in Annex III but only performs a narrow procedural or preparatory task, or improves or checks a human decision, without profiling. The provider documents why.
4. **Transparency only** if it talks to people (Art. 50(1)); otherwise **minimal risk**, with AI literacy as the one duty.

## 2. What applies, and when

| Obligation | Article | From | Systems | Status |
|---|---|---:|---:|---|
| AI literacy of the staff who operate or use it | Art. 4 | 2 February 2025 | 11 | In force |
| Stop the prohibited use | Art. 5(1)(f) | 2 February 2025 | 1 | In force |
| People told they are talking to an AI: the supplier's duty, checked by the employer | Art. 50(1) | 2 August 2026 | 2 | In force |
| Use as instructed, with named human oversight | Art. 26(1)-(2) | 2 December 2027 | 7 | Ahead |
| Input data relevant and representative | Art. 26(4) | 2 December 2027 | 7 | Ahead |
| Monitor; report risks and serious incidents; suspend | Art. 26(5) | 2 December 2027 | 7 | Ahead |
| Keep the logs for at least six months | Art. 26(6) | 2 December 2027 | 7 | Ahead |
| Tell workers' representatives and affected workers before use | Art. 26(7) | 2 December 2027 | 5 | Ahead |
| Data protection impact assessment built on the provider's information | Art. 26(9); GDPR Art. 35 | 2 December 2027 | 7 | Ahead |
| Tell the people decisions are made about | Art. 26(11) | 2 December 2027 | 6 | Ahead |
| Explain a decision on request | Art. 86 | 2 December 2027 | 6 | Ahead |
| Provider duties for a system built in-house | Art. 3(3), 16 | 2 December 2027 | 1 | Ahead |
| Not-high-risk assessment documented | Art. 6(4) | 2 December 2027 | 1 | Ahead |
| Fundamental rights impact assessment before first use, results notified | Art. 27(1)-(4) | 2 December 2027 | 0 | Ahead |
| Register the use in the EU database; do not use an unregistered system | Art. 26(8), 49(3) | 2 December 2027 | 0 | Ahead |

Considered and not applicable:

- **Fundamental rights impact assessment for credit and insurance systems** (Art. 27(1); Annex III 5(b)-(c)). Owed whatever the deployer for credit scoring and life and health insurance pricing; no HR system is one of them. For public bodies and public-service entities it is obligation O14.
- **Annex III point 3, education and vocational training** (Annex III, 3). Covers education and vocational training institutions; an employer's course suggestions that do not feed promotion or pay are not in it.

## 3. Telling the workers, country by country

The AI Act adds its own duty for high-risk systems from December 2027: inform workers' representatives and the affected workers before use (Art. 26(7)), for 5 systems here. The national rules below apply now, and they reach further than the AI Act's high-risk list.

**IT · Milan**

- **Information on fully automated decision or monitoring systems** (D.lgs. 152/1997 art. 1-bis co. 1-6; L. 132/2025 art. 11): Shift scheduling optimiser. In writing, to each worker and to the union representatives (RSA/RSU): the aspects of the job affected, purposes, logic and functioning, data and main parameters, control and correction measures, accuracy, robustness and cybersecurity, possible discriminatory effects; in a structured, machine-readable format; before work starts; at least 24 hours before any change to that information.
- **Agreement or authorisation for tools that allow remote monitoring** (Statuto dei lavoratori, art. 4): Customer service performance analytics. Only for organisational and production needs, safety or protection of company assets, and with an agreement with the union representatives or, failing that, authorisation by the labour inspectorate; tools used to do the work and attendance records are exempt; the data can be used only with adequate information to workers; before the tool is installed.

**PL · Kraków**

- **Notice of monitoring other than video** (Kodeks pracy art. 22³ §4 with art. 22² §§6-10): Customer service performance analytics. Allowed only where needed for full use of working time and proper use of work tools; purpose, scope and method in the workplace rules; at least two weeks before it starts; new hires in writing before they start.

**DE · Munich**

- **Information and consultation on planned AI in work procedures** (BetrVG §90(1) Nr. 3, §90(2)): CV screening and ranking, Targeted job advertising, Interview scheduling assistant, Customer service performance analytics, Shift scheduling optimiser, Attrition-risk model, Pay review recommender, HR service chatbot, Learning recommendations, Writing and translation assistant, Internal mobility matching. Inform the works council with the documents, and consult it while its views can still change the plan; at the planning stage.
- **Co-determination on technical devices able to monitor conduct or performance** (BetrVG §87(1) Nr. 6): Customer service performance analytics, Shift scheduling optimiser, Attrition-risk model, Pay review recommender, Internal mobility matching. A works agreement; without it the system cannot lawfully be used. Courts read 'able to' broadly, so systems that log identifiable use may also need one; before introduction.
- **Co-determination on selection guidelines** (BetrVG §95(1); (2a) where AI helps draw them up): CV screening and ranking, Internal mobility matching. Works council consent to the selection criteria the system applies; before use in hiring, transfer or dismissal decisions.
- **An expert for the works council, deemed necessary for AI** (BetrVG §80(3)): CV screening and ranking, Targeted job advertising, Interview scheduling assistant, Customer service performance analytics, Shift scheduling optimiser, Attrition-risk model, Pay review recommender, HR service chatbot, Learning recommendations, Writing and translation assistant, Internal mobility matching. An expert, agreed with the employer as to person, subject and cost; for AI its necessity is presumed; when the works council assesses the system.

**ES · Barcelona**

- **Information on the parameters of algorithms affecting work** (Estatuto de los Trabajadores art. 64.4.d): CV screening and ranking, Targeted job advertising, Customer service performance analytics, Shift scheduling optimiser, Attrition-risk model, Pay review recommender, Internal mobility matching. The parameters, rules and instructions the system is based on, to the works council; with the periodicity that applies; before use is the prudent reading.

**Five more countries, for an employer elsewhere.** The register also holds 12 rules for France, Netherlands, Ireland, Austria and Belgium: the CSE in France (information before recruitment techniques and automated HR processing are used, consultation before monitoring), the works council's advice and consent in the Netherlands (void without consent), consent in Austria (one replaceable by the conciliation board, one not), three months' notice for a new technology in Belgium, and Ireland's information and consultation forum where one exists. None applies to this employer; the [browser tool](https://d0m3n1c0x.github.io/ai-act-hr-readiness-kit/tool/) runs them on any list of systems.

The [worker information pack](../docs/worker-information.md) has, for each country, who to tell, what the notice must contain and a model text.

## 4. What to ask each supplier

Most deployer duties can only be met with facts the supplier holds. The register turns them into 16 questions and sends each system's supplier the ones its class calls for: 94 in all, most of them for the 6 bought high-risk systems. In-house systems are asked of the team that built them.

| Question | Article | Systems |
|---|---|---:|
| Send the instructions for use, with every item Article 13(3) lists | Art. 13(2)-(3); 26(1) | 6 |
| State the accuracy, robustness and cybersecurity levels the system was tested against, with the metrics, and the circumstances known to affect them | Art. 13(3)(b)(ii)-(iii) | 6 |
| Give the system's performance for the groups of people it is used on | Art. 13(3)(b)(v) | 6 |
| Describe the human oversight measures and the tools that help interpret the output | Art. 13(3)(d); 14; 26(2) | 6 |
| Specify the input data the system expects, and the data it was trained, validated and tested on | Art. 13(3)(b)(vi); 26(4) | 6 |
| Explain how we collect, store and read the logs, and confirm they can be kept at least six months | Art. 12; 13(3)(f); 26(6) | 6 |
| List the changes pre-determined at conformity assessment and commit to tell us before any significant design change | Art. 13(3)(c); 111(2) | 6 |
| Name the contact and the procedure for reporting risks and serious incidents | Art. 26(5); 72; 73 | 6 |
| Provide the information we need for the data protection impact assessment | Art. 13; 26(9); GDPR Art. 35 | 6 |
| Explain what the system can show to explain an individual output | Art. 13(3)(b)(iv); 86 | 5 |
| Confirm the conformity assessment, the EU declaration of conformity, the CE marking and the registration in the EU database | Art. 16(f)-(i); 47-49 | 6 |
| Send the documented assessment that the system is not high-risk, and its registration | Art. 6(4); 49(2) | 1 |
| Confirm people are told they are dealing with an AI, and put it in the contract | Art. 50(1) | 2 |
| Confirm the system does not infer emotions, and will not without telling us first | Art. 5(1)(f) | 10 |
| Provide the logic, main parameters and data categories the national notices to workers require | IT D.lgs. 152/1997 art. 1-bis co. 2; ES ET art. 64.4.d; AT ArbVG §91(2) | 6 |
| Provide training material for the people who will operate and use it | Art. 4 | 10 |

The [supplier questionnaire](../deliverables/supplier_questionnaire.md) lists them system by system, ready to send.

## 5. AI literacy: who learns what

Since the Digital Omnibus, Article 4 asks providers and deployers to *take measures to support* the AI literacy of the people who operate and use their systems, taking into account their knowledge and the context, without guaranteeing any level. The register maps each system to the modules its answers call for:

| Module | For whom | Systems |
|---|---|---:|
| Working with this system | Everyone who operates or uses it | 11 |
| Overseeing a high-risk system | The named overseers | 7 |
| Decisions about people | Recruiters, managers and HR business partners who decide | 6 |
| Monitoring and workers' rights | Line managers and HR operations | 1 |
| AI that talks to people | The owners of chatbots and assistants | 2 |
| Building a high-risk system | The data and IT team that built it | 1 |

Evidence to keep: date, material and attendance for each module and person: the measures taken, not a level reached (Art. 4(1) as replaced by Reg. 2026/1744). The [literacy plan](../deliverables/ai_literacy_plan.md) gives the modules per system.

## 6. The fundamental rights impact assessment

**Not owed here, drafted anyway.** Article 27 asks for the assessment before the first use of a high-risk system by bodies governed by public law and private entities providing public services (and by deployers of credit and life and health insurance systems, which no HR system is). The deployer here is a private employer, so obligation O14 is off; the kit still drafts the assessment for its 7 high-risk systems, because the questions it asks are the ones a works council, a data protection authority or a court will ask, and because a public employer running the tool will owe it.

Since Regulation 2026/1744 the assessment may cross-refer to the data protection impact assessment where that already covers an element (Art. 27(4) as replaced). The six elements, and the section of a GDPR Article 35(7) assessment that usually holds each:

| Art. 27(1) | Element | DPIA (Art. 35(7)) | In the kit |
|---|---|---|---|
| (a) | The deployer's processes in which the system is used, in line with its intended purpose | 35(7)(a) | Register: HR function and rationale |
| (b) | The period of time and the frequency of use | 35(7)(a) | To complete: not in the register |
| (c) | The categories of people and groups likely to be affected | 35(7)(a), (c) | Register: applicants or employees, countries, department, workers in scope |
| (d) | The specific risks of harm to them, using the provider's Article 13 information | 35(7)(c) | Supplier answers V02-V03; the boundary cases in the report |
| (e) | How the human oversight measures of the instructions for use are put in place | 35(7)(d) | Obligation O04; supplier answer V04; literacy module L02 |
| (f) | The measures if the risks materialise: internal governance and complaint mechanisms | 35(7)(d) | Obligations O06 and O11; supplier answer V08 |

A public body also registers its use of each high-risk system in the EU database and may not use one the provider has not registered (Art. 26(8), 49(3)), and its legacy systems comply by 2 August 2030 whatever their design changes (Art. 111(2)). The [draft assessments](../deliverables/fria_drafts.md) are pre-filled from the register, one per high-risk system.

## 7. The judgement calls

- **Shift scheduling is a boundary case.** On availability and certified skills alone it might not evaluate anyone; past attendance makes it allocate tasks on individual behaviour, which is profiling. The register classifies it as high-risk, and a supplier that drops attendance from the inputs would change the answer.
- **The interview scheduler is not high-risk, on the provider's word.** It performs a narrow procedural task (Art. 6(3)(a)), but the documented assessment is the provider's to make (Art. 6(4)); the employer should hold a copy, and revisit it if the tool starts ranking candidates.
- **The pay review recommender sits under two laws.** It is high-risk under the AI Act (Annex III 4(b)), and its pay-setting criteria must be objective and gender-neutral under the Pay Transparency Directive (Art. 4(4) and 6(1)), whose categories and 5% screen are in [pay-transparency-readiness-kit](https://github.com/D0M3N1C0X/pay-transparency-readiness-kit).
- **Learning recommendations stay minimal only while they do not count.** If course completion fed promotion or pay, the system would move into Annex III 4(b).
- **The right to an explanation (Art. 86)** is in a chapter that applies from August 2026, but it attaches to decisions based on high-risk Annex III systems, a classification that applies from December 2027. The register dates it with the high-risk duties; the reading should be confirmed. It also applies only where Union law gives no such right already (Art. 86(3)), and GDPR Art. 15(1)(h) and 22 often do.
- **Systems already in use and Article 111(2).** The grace period follows the type and model, not the employer's installation (recital 39 of Reg. 2026/1744): a system on the market before 2 December 2027 stays outside the high-risk duties until its design changes significantly. The register keeps the duties on the list, because a supplier's next major release, or a retrained in-house model, ends the grace period.
- **Applicant-only systems and Italy's notice.** Art. 1-bis of D.lgs. 152/1997 informs the worker, so the register leaves out systems used only on applicants, such as ad targeting; candidates who are hired are told at hiring. A cautious employer tells them anyway.
- **Data protection law does not wait for 2027.** A data protection impact assessment is already owed for high-risk processing of employees' data (GDPR Art. 35); from December 2027 the AI Act adds that it must use the provider's information (Art. 26(9)). For fully automated systems, GDPR Art. 22 already limits decisions based solely on automated processing.
- **Germany's co-determination is the binding constraint now.** A system able to monitor conduct or performance needs a works agreement before it is introduced (BetrVG §87(1) Nr. 6); 5 systems here process performance data of workers in Munich, and courts read "able to" broadly enough that a chatbot or assistant logging who used it may need one too.

- **The new countries' rules are read conservatively.** Whether an HR AI system is a *nouvelle technologie* (France), an *important* technological facility (Netherlands), a system touching human dignity (Austria) or an *investment* in a new technology (Belgium) is a judgement; the register assumes yes where the system monitors or changes work, and names it in the verification register.

## 8. The next 90 days

1. **Stop the video interview analysis pilot** in Barcelona, delete the scores, and tell the supplier and the candidates assessed.
2. **Decide the attrition-risk model's future**: keep it and build the provider's file, buy a supplier's equivalent, or narrow it to a team-level view that profiles no one.
3. **Open the works council agenda in Munich** with the information and co-determination items, and send the Spanish works council the parameters of the systems that affect work.
4. **Send the Italian notices** for the fully automated systems and settle the agreement for the monitoring tool; give the Polish notice two weeks before any new monitoring.
5. **Put AI literacy on record**: run the 28 module-system pairs of the literacy plan and keep who took which, when, with what material.
6. **Send the supplier questionnaire**: 94 questions, starting with the instructions for use and the information the data protection impact assessments need; name an overseer per high-risk system.
7. **Complete the draft fundamental rights assessments** with the DPO, cross-referring to the DPIAs.

## 9. Method, sources and limits

- **Two engines, one answer.** Every class, role and obligation is computed in Python and again by live formulas in [the register workbook](../deliverables/ai_act_hr_register.xlsx); its Reconciliation sheet checks each pair, and CI recalculates the workbook with LibreOffice.
- **Law read in the original.** The AI Act and the Digital Omnibus in the Official Journal; the Italian, German and Spanish rules on the official legal databases; the Dutch and Austrian ones through their governments' open-data services, the French on the Ministry of Labour's official code, the Irish in the Irish Statute Book and the Belgian agreements on the National Labour Council's site; the Polish ones through secondary sources. Each statement has its status in [docs/verification.md](../docs/verification.md).
- **Limits.** Invented systems and answers; the classification follows the text of the Regulation, and Commission guidelines, harmonised standards or national practice can move boundary cases. Not legal advice.

