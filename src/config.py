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
ENTITIES = {"IT": "IT · Milan", "PL": "PL · Kraków", "DE": "DE · Munich", "ES": "ES · Barcelona"}
COUNTRIES = list(ENTITIES)
DEPARTMENTS = ["Customer Service", "Finance", "HR", "Operations", "Sales", "Tech"]
CHOICES = {"supplier": ["Vendor", "In-house"], "annex_iii": ["None", "4(a)", "4(b)"],
           "art6_3_condition": ["None", "(a)", "(b)", "(c)", "(d)"]}

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
# Article 111(2), as amended: a high-risk system whose type and model was on the market before D_ANNEX_III falls under
# the Regulation only once its design changes significantly (Reg. 2026/1744, Art. 1(39) and recital 39).

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
]
OBLIGATION_KEYS = [o[0] for o in OBLIGATIONS]

# Considered and left out, with the reason, so the register shows it was looked at.
NOT_APPLICABLE = [
    ("Fundamental rights impact assessment", "Art. 27",
     "Owed by public bodies, private entities providing public services, and deployers of credit and insurance "
     "systems (Annex III 5(b)-(c)). A private employer using HR systems is none of these."),
    ("Registration of the use in the EU database", "Art. 26(8), 49(3)",
     "Owed by deployers that are public authorities. A provider registers its own systems (Art. 49(1)), which here "
     "means the in-house attrition model."),
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
]
WORKER_KEYS = [r[0] for r in WORKER_RULES]
