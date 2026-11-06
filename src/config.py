"""
Every date, rule and assumption the kit uses, with its source. Article numbers are those of Regulation (EU)
2024/1689 (the AI Act) as amended by Regulation (EU) 2026/1744 (the Digital Omnibus on AI), both read in the
Official Journal; national rules are in docs/verification.md with their status.
"""
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SYSTEMS = DATA / "ai_systems.csv"
HEADCOUNT = DATA / "source" / "headcount.csv"
DELIVERABLES = ROOT / "deliverables"
REPORTS = ROOT / "reports"

# The headcount comes from the payroll extract of pay-transparency-readiness-kit at this commit, so the two kits
# describe the same organisation (3,443 workers active on 30 June 2026).
SOURCE_REPO = "pay-transparency-readiness-kit"
SOURCE_COMMIT = "0bfb9c9"
SOURCE_SHA256 = "647531fa917a4f74"

ASSESSMENT_DATE = date(2026, 10, 24)
# The employer of the dry run has four entities; the register knows the rules of nine countries, so the browser tool
# and the workbook work for an employer anywhere in them.
ENTITIES = {"IT": "IT · Milan", "PL": "PL · Kraków", "DE": "DE · Munich", "ES": "ES · Barcelona"}
COUNTRY_NAMES = {"IT": "Italy", "PL": "Poland", "DE": "Germany", "ES": "Spain", "FR": "France", "NL": "Netherlands",
                 "IE": "Ireland", "AT": "Austria", "BE": "Belgium"}
COUNTRIES = list(COUNTRY_NAMES)
DEPARTMENTS = ["Customer Service", "Finance", "HR", "Operations", "Sales", "Tech"]
CHOICES = {"supplier": ["Vendor", "In-house"], "annex_iii": ["None", "4(a)", "4(b)"],
           "art6_3_condition": ["None", "(a)", "(b)", "(c)", "(d)"]}

# ---- Who the deployer is (Article 27(1), Article 26(8), Article 111(2)) ----------------------------------------------
# One answer for the whole organisation. The dry run's employer is private, so the fundamental rights impact
# assessment is not owed and the kit drafts a voluntary one (docs/fria.md).
PRIVATE = "Private employer"
PUBLIC_BODY = "Public body"
PUBLIC_SERVICE = "Private entity providing public services"
DEPLOYER_TYPES = [PRIVATE, PUBLIC_BODY, PUBLIC_SERVICE]
DEPLOYER = PRIVATE

# ---- Classification (Articles 5, 6 and 50) ----------------------------------------------------------------------
PROHIBITED = "Prohibited"
HIGH_RISK = "High-risk"
DEROGATION = "Not high-risk (Art. 6(3))"
TRANSPARENCY = "Transparency only"
MINIMAL = "Minimal risk"
CLASSES = [PROHIBITED, HIGH_RISK, DEROGATION, TRANSPARENCY, MINIMAL]

# ---- Application dates (Article 113, as amended by Regulation (EU) 2026/1744, Article 1(40)) -----------------------
D_CHAPTERS_I_II = date(2025, 2, 2)      # Articles 4 and 5
D_GENERAL = date(2026, 8, 2)            # the rest, Article 50 included, unless listed below
D_ANNEX_III = date(2027, 12, 2)         # Chapter III Sections 1-3 for Annex III systems: Articles 6 to 27
D_PUBLIC_LEGACY = date(2030, 8, 2)      # Art. 111(2), last sentence: systems intended for public authorities
# Article 111(2), as amended: a high-risk system whose type and model was on the market before D_ANNEX_III falls under
# the Regulation only once its design changes significantly (Reg. 2026/1744, Art. 1(39) and recital 39); those intended
# to be used by public authorities comply by 2 August 2030 in any case.

# ---- Obligations ----------------------------------------------------------------------------------------------------
# key: (short name, article, applies when, from, who acts, evidence a reviewer would ask for)
# "applies when" is evaluated per system by obligations.applies() and, with the same logic, by Excel formulas.
OBLIGATIONS = [
    ("O01", "AI literacy of the staff who operate or use it", "Art. 4", "in use", D_CHAPTERS_I_II, "Deployer",
     "Training plan per system and role; measures taken, not a guaranteed level (wording of Reg. 2026/1744)"),
    ("O02", "Stop the prohibited use", "Art. 5(1)(f)", "prohibited", D_CHAPTERS_I_II, "Deployer",
     "Decision to stop, date, data deleted, supplier told"),
    ("O03", "People told they are talking to an AI: the supplier's duty, checked by the employer", "Art. 50(1)", "interacts", D_GENERAL, "Provider; deployer checks",
     "Screenshot of the notice; clause in the supplier contract"),
    ("O04", "Use as instructed, with named human oversight", "Art. 26(1)-(2)", "high-risk", D_ANNEX_III, "Deployer",
     "Instructions for use on file; named overseers with training and authority to override"),
    ("O05", "Input data relevant and representative", "Art. 26(4)", "high-risk and input", D_ANNEX_III, "Deployer",
     "Data checks before each run; who owns the input"),
    ("O06", "Monitor; report risks and serious incidents; suspend", "Art. 26(5)", "high-risk", D_ANNEX_III, "Deployer",
     "Monitoring routine; incident procedure with the supplier's contact"),
    ("O07", "Keep the logs for at least six months", "Art. 26(6)", "high-risk", D_ANNEX_III, "Deployer",
     "Retention setting; who can read the logs"),
    ("O08", "Tell workers' representatives and affected workers before use", "Art. 26(7)", "high-risk at work",
     D_ANNEX_III, "Employer", "Dated notice to representatives and workers, through the national procedure"),
    ("O09", "Data protection impact assessment built on the provider's information", "Art. 26(9); GDPR Art. 35",
     "high-risk", D_ANNEX_III, "Deployer", "DPIA signed off by the DPO; provider's Article 13 information attached"),
    ("O10", "Tell the people decisions are made about", "Art. 26(11)", "high-risk and decides", D_ANNEX_III, "Deployer",
     "Notice in the candidate or employee journey"),
    ("O11", "Explain a decision on request", "Art. 86", "high-risk and decides", D_ANNEX_III, "Deployer",
     "Explanation template; who answers and how fast"),
    ("O12", "Provider duties for a system built in-house", "Art. 3(3), 16", "high-risk in-house", D_ANNEX_III,
     "Employer as provider", "Quality management, technical documentation, conformity assessment, EU registration"),
    ("O13", "Not-high-risk assessment documented", "Art. 6(4)", "derogation", D_ANNEX_III, "Provider; deployer keeps it",
     "The provider's documented assessment, on file"),
    ("O14", "Fundamental rights impact assessment before first use, results notified", "Art. 27(1)-(4)",
     "high-risk and public", D_ANNEX_III, "Deployer",
     "The six elements of Art. 27(1), cross-referenced to the DPIA (Art. 27(4) as amended); notification to the "
     "market surveillance authority with the AI Office template (Art. 27(3), (5))"),
    ("O15", "Register the use in the EU database; do not use an unregistered system", "Art. 26(8), 49(3)",
     "high-risk and public body", D_ANNEX_III, "Deployer",
     "Registration record of the use; check that the provider registered the system (Art. 49(1))"),
]
OBLIGATION_KEYS = [o[0] for o in OBLIGATIONS]

# Considered and left out, with the reason, so the register shows it was looked at.
NOT_APPLICABLE = [
    ("Fundamental rights impact assessment for credit and insurance systems", "Art. 27(1); Annex III 5(b)-(c)",
     "Owed whatever the deployer for credit scoring and life and health insurance pricing; no HR system is one of "
     "them. For public bodies and public-service entities it is obligation O14."),
    ("Annex III point 3, education and vocational training", "Annex III, 3",
     "Covers education and vocational training institutions; an employer's course suggestions that do not feed "
     "promotion or pay are not in it."),
]

# ---- Telling the workers: national rules ---------------------------------------------------------------------------
# key: (country, rule, source, applies when, what it asks, when)
WORKER_RULES = [
    ("W-IT1", "IT", "Information on fully automated decision or monitoring systems",
     "D.lgs. 152/1997 art. 1-bis co. 1-6; L. 132/2025 art. 11", "fully automated",
     "In writing, to each worker and to the union representatives (RSA/RSU): the aspects of the job affected, purposes, "
     "logic and functioning, data and main parameters, control and correction measures, accuracy, robustness and "
     "cybersecurity, possible discriminatory effects; in a structured, machine-readable format",
     "Before work starts; at least 24 hours before any change to that information"),
    ("W-IT2", "IT", "Agreement or authorisation for tools that allow remote monitoring", "Statuto dei lavoratori, art. 4",
     "monitors", "Only for organisational and production needs, safety or protection of company assets, and with an "
     "agreement with the union representatives or, failing that, authorisation by the labour inspectorate; tools used "
     "to do the work and attendance records are exempt; the data can be used only with adequate information to workers",
     "Before the tool is installed"),
    ("W-DE1", "DE", "Information and consultation on planned AI in work procedures", "BetrVG §90(1) Nr. 3, §90(2)",
     "in the country", "Inform the works council with the documents, and consult it while its views can still change "
     "the plan", "At the planning stage"),
    ("W-DE2", "DE", "Co-determination on technical devices able to monitor conduct or performance", "BetrVG §87(1) Nr. 6",
     "processes performance", "A works agreement; without it the system cannot lawfully be used. Courts read 'able to' "
     "broadly, so systems that log identifiable use may also need one", "Before introduction"),
    ("W-DE3", "DE", "Co-determination on selection guidelines", "BetrVG §95(1); (2a) where AI helps draw them up",
     "selects", "Works council consent to the selection criteria the system applies", "Before use in hiring, transfer "
     "or dismissal decisions"),
    ("W-DE4", "DE", "An expert for the works council, deemed necessary for AI", "BetrVG §80(3)",
     "in the country", "An expert, agreed with the employer as to person, subject and cost; for AI its necessity is "
     "presumed", "When the works council assesses the system"),
    ("W-ES1", "ES", "Information on the parameters of algorithms affecting work", "Estatuto de los Trabajadores art. 64.4.d",
     "affects work", "The parameters, rules and instructions the system is based on, to the works council",
     "With the periodicity that applies; before use is the prudent reading"),
    ("W-PL1", "PL", "Notice of monitoring other than video", "Kodeks pracy art. 22³ §4 with art. 22² §§6-10",
     "monitors", "Allowed only where needed for full use of working time and proper use of work tools; purpose, scope "
     "and method in the workplace rules", "At least two weeks before it starts; new hires in writing before they start"),
    ("W-FR1", "FR", "Information and consultation of the social and economic committee on AI in HR",
     "Code du travail L2312-38 al. 1-2, L2312-8 II 4°, L2315-94 2°", "in the country",
     "In undertakings with at least 50 employees (L2312-1): inform the CSE before using methods or techniques that "
     "help recruit candidates and before introducing automated personnel management processing; consult it on the "
     "introduction of new technologies, with precise written information and enough time (L2312-15); it may "
     "appoint an expert", "Before use; consultation while the CSE's opinion can still be taken into account"),
    ("W-FR2", "FR", "Information and consultation before means of monitoring employees' activity",
     "Code du travail L2312-38 al. 3, L2312-37 1°, L1121-1", "monitors",
     "Inform and consult the CSE before deciding to use means or techniques that allow employees' activity to be "
     "monitored; any restriction of rights must be justified by the task and proportionate to its aim",
     "Before the decision to implement"),
    ("W-FR3", "FR", "Tell each candidate and employee before the method is used on them",
     "Code du travail L1221-8, L1221-9, L1222-3, L1222-4", "in the country",
     "Candidates expressly told of the recruitment methods and techniques used on them, employees of the evaluation "
     "methods; no personal information collected by a device not brought to their knowledge first; methods relevant "
     "to their purpose; results confidential", "Before the method is used on the person"),
    ("W-NL1", "NL", "Works council advice on an important technological facility", "WOR art. 25(1)(k), (2)-(6)",
     "in the country", "In undertakings with at least 50 persons (art. 2): submit the proposed decision in writing "
     "with its reasons and expected consequences for staff; if the decision departs from the advice, wait a month "
     "before carrying it out", "Early enough for the advice to influence the decision materially"),
    ("W-NL2", "NL", "Works council consent on personal data, monitoring and staff assessment",
     "WOR art. 27(1)(g), (k), (l), (5)", "on employees",
     "Consent to the arrangement on processing and protecting staff personal data (k), on facilities able to observe "
     "or check attendance, behaviour or performance (l) and on staff assessment (g); a decision taken without consent "
     "or the cantonal court's permission is void if the works council invokes it in writing within a month",
     "Before the arrangement is adopted or changed"),
    ("W-NL3", "NL", "Works council consent on hiring, dismissal or promotion policy", "WOR art. 27(1)(e), (5)",
     "selects", "Consent to an arrangement on hiring, dismissal or promotion policy, which the system's selection "
     "criteria put into practice; without it the decision can be declared void", "Before use in hiring or promotion"),
    ("W-IE1", "IE", "Information and consultation forum, where one has been set up",
     "Employees (Provision of Information and Consultation) Act 2006, s. 4, 7, 10, Schedule 1 para. 3(c)",
     "changes work organisation", "In undertakings with at least 50 employees that have an information and "
     "consultation arrangement (agreed, or the Standard Rules after a request by 10% of employees): information and "
     "consultation on decisions likely to lead to substantial changes in work organisation. Without one, Irish law "
     "adds no general duty; Art. 26(7) still applies to high-risk systems",
     "Under the arrangement; before the decision is the prudent reading"),
    ("W-AT1", "AT", "Tell the works council which employee data are processed automatically", "ArbVG §91(2), §92(1)",
     "on employees", "Tell the works council what kinds of employee personal data are recorded automatically and which "
     "processing and transfers are planned; on request let it check their basis; discuss it in the joint "
     "consultations", "Before processing starts"),
    ("W-AT2", "AT", "Works council consent for personal data and assessment systems, replaceable by the conciliation "
     "board", "ArbVG §96a(1) Z 1-2, (2)", "on employees",
     "Consent to systems that process employees' personal data beyond general personal details and qualifications, "
     "unless the use goes no further than duties under law, collective rules or the contract, and to systems for "
     "assessing employees; the conciliation board can replace a refused consent",
     "Before introduction: without consent the measure has no legal effect"),
    ("W-AT3", "AT", "Works council consent for control systems that touch human dignity, not replaceable",
     "ArbVG §96(1) Z 3, (2)", "monitors", "Consent to control measures and technical systems for monitoring employees "
     "that touch human dignity; no body can replace it, and a works agreement without a term can be ended at any time",
     "Before introduction: without consent the measure has no legal effect"),
    ("W-BE1", "BE", "Written information and consultation on a new technology with collective consequences",
     "CCT n° 39 of 13 December 1983, art. 1-6", "changes work organisation",
     "In undertakings with on average at least 50 workers, where at least 50% and 10 workers of the categories "
     "affected see their work change: written information on the technology, why it is introduced and its social "
     "consequences, and consultation of the works council or, failing that, the union delegation; failing that, "
     "dismissals linked to the technology are barred and cost three months' pay",
     "At the latest three months before implementation starts"),
    ("W-BE2", "BE", "Information before monitoring electronic online communications",
     "CCT n° 81 of 26 April 2002, art. 5, 7, 8", "monitors",
     "Monitoring of network communication data only for the four purposes listed, stated explicitly; inform the "
     "works council (failing that the prevention committee, the union delegation or the workers) and each worker "
     "concerned of every aspect of the monitoring", "Before the monitoring system is installed"),
]
WORKER_KEYS = [r[0] for r in WORKER_RULES]

# ---- Questions for the supplier --------------------------------------------------------------------------------------
# What the employer can only do with the supplier's help, asked before signing or at renewal. Each question applies to
# systems bought from a vendor (an in-house system is asked of the team that built it) when its condition holds.
# key: (question, article, applies when, why the employer needs the answer)
VENDOR_QUESTIONS = [
    ("V01", "Send the instructions for use, with every item Article 13(3) lists", "Art. 13(2)-(3); 26(1)",
     "high-risk", "Using the system as instructed is the first deployer duty"),
    ("V02", "State the accuracy, robustness and cybersecurity levels the system was tested against, with the metrics, "
     "and the circumstances known to affect them", "Art. 13(3)(b)(ii)-(iii)", "high-risk",
     "Monitoring, the DPIA and the Italian and Spanish notices need them"),
    ("V03", "Give the system's performance for the groups of people it is used on", "Art. 13(3)(b)(v)", "high-risk",
     "The check for discriminatory effects starts here"),
    ("V04", "Describe the human oversight measures and the tools that help interpret the output",
     "Art. 13(3)(d); 14; 26(2)", "high-risk", "The named overseers are trained on them"),
    ("V05", "Specify the input data the system expects, and the data it was trained, validated and tested on",
     "Art. 13(3)(b)(vi); 26(4)", "high-risk and input", "Input data must be relevant and representative"),
    ("V06", "Explain how we collect, store and read the logs, and confirm they can be kept at least six months",
     "Art. 12; 13(3)(f); 26(6)", "high-risk", "Log retention is a deployer duty"),
    ("V07", "List the changes pre-determined at conformity assessment and commit to tell us before any significant "
     "design change", "Art. 13(3)(c); 111(2)", "high-risk on the market",
     "A significant change ends the grace period of Art. 111(2)"),
    ("V08", "Name the contact and the procedure for reporting risks and serious incidents", "Art. 26(5); 72; 73",
     "high-risk", "The employer must inform the provider without undue delay"),
    ("V09", "Provide the information we need for the data protection impact assessment", "Art. 13; 26(9); GDPR Art. 35",
     "high-risk", "The DPIA is built on the provider's information"),
    ("V10", "Explain what the system can show to explain an individual output", "Art. 13(3)(b)(iv); 86",
     "high-risk and decides", "The person concerned can ask for an explanation"),
    ("V11", "Confirm the conformity assessment, the EU declaration of conformity, the CE marking and the registration "
     "in the EU database", "Art. 16(f)-(i); 47-49", "high-risk",
     "A public employer may not use an unregistered system (Art. 26(8))"),
    ("V12", "Send the documented assessment that the system is not high-risk, and its registration",
     "Art. 6(4); 49(2)", "derogation", "The employer keeps it on file and relies on it"),
    ("V13", "Confirm people are told they are dealing with an AI, and put it in the contract", "Art. 50(1)",
     "interacts", "The duty is the provider's; the employer checks it"),
    ("V14", "Confirm the system does not infer emotions, and will not without telling us first", "Art. 5(1)(f)",
     "in use", "Emotion recognition at work is prohibited"),
    ("V15", "Provide the logic, main parameters and data categories the national notices to workers require",
     "IT D.lgs. 152/1997 art. 1-bis co. 2; ES ET art. 64.4.d; AT ArbVG §91(2)", "high-risk or monitors",
     "The employer writes the notices; the supplier holds the facts"),
    ("V16", "Provide training material for the people who will operate and use it", "Art. 4", "in use",
     "AI literacy measures for staff"),
]
VENDOR_KEYS = [q[0] for q in VENDOR_QUESTIONS]

# ---- AI literacy (Article 4, as replaced by Regulation 2026/1744) -----------------------------------------------------
# Measures that support the literacy of the people who operate and use each system; the employer documents what it
# did, not a level reached (Art. 4(1), last sentence). key: (module, for whom, applies when, what it covers)
LITERACY = [
    ("L01", "Working with this system", "Everyone who operates or uses it", "in use",
     "What it does and does not do, its known limits, when not to rely on it, how to report a problem"),
    ("L02", "Overseeing a high-risk system", "The named overseers", "high-risk",
     "Reading the output, automation bias, the authority to override or stop it, logs and incidents (Art. 14, 26(2))"),
    ("L03", "Decisions about people", "Recruiters, managers and HR business partners who decide",
     "high-risk and decides", "Telling the person (Art. 26(11)), explaining a decision on request (Art. 86), human "
     "review"),
    ("L04", "Monitoring and workers' rights", "Line managers and HR operations", "monitors",
     "Purpose and proportionality, what the data may and may not be used for, the national rules on telling workers"),
    ("L05", "AI that talks to people", "The owners of chatbots and assistants", "interacts",
     "Saying it is an AI, handing over to a person, what it must not answer"),
    ("L06", "Building a high-risk system", "The data and IT team that built it", "high-risk in-house",
     "Provider duties (Art. 16), data governance, documentation, and why a retrained model is a significant change"),
]
LITERACY_KEYS = [m[0] for m in LITERACY]
LITERACY_EVIDENCE = ("Date, material and attendance for each module and person: the measures taken, not a level "
                     "reached (Art. 4(1) as replaced by Reg. 2026/1744)")

# ---- The fundamental rights impact assessment (Article 27) -----------------------------------------------------------
# The six elements of Art. 27(1), and the section of a GDPR Article 35(7) DPIA that may already cover each one: since
# Reg. 2026/1744 the deployer may cross-refer to it (Art. 27(4) as replaced). The mapping is the kit's reading.
# key: (element, DPIA section that may cover it, where the kit already holds the facts)
FRIA_ELEMENTS = [
    ("(a)", "The deployer's processes in which the system is used, in line with its intended purpose", "35(7)(a)",
     "Register: HR function and rationale"),
    ("(b)", "The period of time and the frequency of use", "35(7)(a)", "To complete: not in the register"),
    ("(c)", "The categories of people and groups likely to be affected", "35(7)(a), (c)",
     "Register: applicants or employees, countries, department, workers in scope"),
    ("(d)", "The specific risks of harm to them, using the provider's Article 13 information", "35(7)(c)",
     "Supplier answers V02-V03; the boundary cases in the report"),
    ("(e)", "How the human oversight measures of the instructions for use are put in place", "35(7)(d)",
     "Obligation O04; supplier answer V04; literacy module L02"),
    ("(f)", "The measures if the risks materialise: internal governance and complaint mechanisms", "35(7)(d)",
     "Obligations O06 and O11; supplier answer V08"),
]
