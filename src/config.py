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

# ---- Obligations ----------------------------------------------------------------------------------------------------
# key: (short name, article, applies when, from, who acts, evidence a reviewer would ask for)
# "applies when" is evaluated per system by obligations.applies() and, with the same logic, by Excel formulas.
OBLIGATIONS = [
    ("O01", "AI literacy of the staff who operate or use it", "Art. 4", "in use", D_CHAPTERS_I_II, "Deployer",
     "Training plan per system and role; measures taken, not a guaranteed level (wording of Reg. 2026/1744)"),
    ("O02", "Stop the prohibited use", "Art. 5(1)(f)", "prohibited", D_CHAPTERS_I_II, "Deployer",
     "Decision to stop, date, data deleted, supplier told"),
    ("O03", "People told they are talking to an AI", "Art. 50(1)", "interacts", D_GENERAL, "Provider; deployer checks",
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
    ("O12", "Provider duties for a system built in-house", "Art. 16 and 25", "high-risk in-house", D_ANNEX_III,
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
]

# ---- Telling the workers: national rules ---------------------------------------------------------------------------
# key: (country, rule, source, applies when, what it asks, when)
WORKER_RULES = [
    ("W-IT1", "IT", "Information on automated decision or monitoring systems", "D.lgs. 152/1997 art. 1-bis; L. 132/2025 art. 11",
     "fully automated", "Purposes, logic, data and parameters, controls, accuracy and possible discriminatory effects, "
     "in writing to each worker and to the union representatives (RSA/RSU)", "Before work starts, or 24 hours before a change"),
    ("W-IT2", "IT", "Agreement or authorisation for tools that can monitor workers", "Statuto dei lavoratori, art. 4",
     "monitors", "An agreement with the union representatives or, failing that, authorisation by the labour inspectorate",
     "Before the tool is installed"),
    ("W-DE1", "DE", "Information and consultation on planned AI in work procedures", "BetrVG §90(1) Nr. 3, §90(2)",
     "used on workers", "Inform the works council with the documents, and consult it while its views can still change the plan",
     "At the planning stage"),
    ("W-DE2", "DE", "Co-determination on technical devices able to monitor conduct or performance", "BetrVG §87(1) Nr. 6",
     "processes performance", "A works agreement; without it the system cannot lawfully be used",
     "Before introduction"),
    ("W-DE3", "DE", "Co-determination on selection guidelines, also when AI is used", "BetrVG §95(1), (2a)",
     "selects", "Works council consent to the selection criteria", "Before use in hiring, transfer or dismissal decisions"),
    ("W-DE4", "DE", "An expert for the works council, deemed necessary for AI", "BetrVG §80(3)",
     "used on workers", "Budget and access for an expert of the works council's choosing", "When the works council assesses the system"),
    ("W-ES1", "ES", "Information on the parameters of algorithms affecting work", "Estatuto de los Trabajadores art. 64.4.d",
     "affects work", "The parameters, rules and instructions the system is based on, to the works council",
     "Before use, and with the periodicity that applies"),
    ("W-PL1", "PL", "Notice of monitoring other than video", "Kodeks pracy art. 22³",
     "monitors", "Purpose, scope and method in the workplace rules; notice to each worker",
     "At least two weeks before it starts"),
]
WORKER_KEYS = [r[0] for r in WORKER_RULES]
