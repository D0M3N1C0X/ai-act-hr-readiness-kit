"""
Writes reports/ai_act_readiness.md, the written read-out, and its HTML page.

Every number in the text comes from src/register.py, the same functions the workbook is reconciled against.
"""
import pandas as pd

import register
import report_html
from config import (
    ASSESSMENT_DATE,
    COUNTRIES,
    COUNTRY_NAMES,
    D_ANNEX_III,
    DEPLOYER,
    ENTITIES,
    FRIA_ELEMENTS,
    HIGH_RISK,
    LITERACY,
    LITERACY_EVIDENCE,
    NOT_APPLICABLE,
    OBLIGATIONS,
    PROHIBITED,
    REPORTS,
    VENDOR_QUESTIONS,
    WORKER_RULES,
)


def day(d) -> str:
    return f"{d.day} {d:%B %Y}"


def md_table(head, rows, align) -> str:
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---:" if a == "r" else "---" for a in align) + "|"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def lower(name: str) -> str:
    """'Shift scheduling optimiser' -> 'shift scheduling optimiser', but 'CV screening' stays as it is."""
    return name if name[:2].isupper() else name[0].lower() + name[1:]


def names(r: pd.DataFrame, mask) -> list[str]:
    return [lower(n) for n in r.loc[mask, "system"]]


WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]


def count(n: int) -> str:
    """A count that opens a sentence, in words."""
    return WORDS[n].capitalize() if n < len(WORDS) else f"{n:,}"


def plural(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def write() -> dict:
    systems = register.load().set_index("system_id")
    r = register.build()
    s = register.summary(r)
    days = (D_ANNEX_III - ASSESSMENT_DATE).days
    banned = r[r["class"] == PROHIBITED].iloc[0]
    provider = r[r["role"] == "Provider and deployer"].iloc[0]
    rule = {k: n for k, n in s["worker_rules"].items()}
    obl = s["obligations"]

    L = []
    add = L.append
    add("# AI Act readiness for HR: what the employer must do, by when, and whom to tell")
    add("")
    add(f"**Scope:** the {s['systems']} AI systems the HR function uses at an employer in Italy, Poland, Germany and "
        f"Spain, with {s['workers_total']:,} workers")
    add("**Method:** each system classified from the answers in the register, in Python and in a live Excel model, "
        "reconciled cell by cell")
    add("**Law:** Regulation (EU) 2024/1689 as amended by Regulation (EU) 2026/1744, both read in the Official "
        f"Journal; national rules on informing and consulting workers in {WORDS[len(COUNTRIES)]} countries: the "
        "employer's four, and France, the Netherlands, Ireland, Austria and Belgium for anyone running the tool")
    add("")
    add("> A dry run, not legal advice. The organisation is the one in "
        "[pay-transparency-readiness-kit](https://github.com/D0M3N1C0X/pay-transparency-readiness-kit); its AI "
        "systems are invented to cover the cases an HR function meets. Boundary cases are named as such.")
    add("")
    add("## The answer")
    add("")
    add(f"- **One system has to stop now.** The {lower(banned['system'])} pilot in Barcelona infers candidates' "
        "emotions from their voice and face. Inferring emotions in the workplace has been prohibited since 2 February "
        "2025 unless it is for medical or safety reasons (Art. 5(1)(f)); the fine reaches €35 million or 7% of "
        "worldwide turnover (Art. 99(3)).")
    add(f"- **{count(s['n_' + HIGH_RISK])} systems are high-risk**: {', '.join(names(r, r['class'] == HIGH_RISK))}. The "
        f"high-risk duties apply from {day(D_ANNEX_III)}, {days} days from this assessment, after the Digital Omnibus "
        f"moved them from 2 August 2026. A system whose type and model was already on the market by then falls under "
        f"them only when its design changes significantly (Art. 111(2), as amended); "
        f"{'all ' + WORDS[s['legacy']] if s['legacy'] == s['n_' + HIGH_RISK] else str(s['legacy'])} are in that position. Cloud HR software changes often, so the safe plan is December 2027.")
    add(f"- **The {lower(provider['system'])} makes the employer a provider.** HR analytics put it into service for the "
        "employer's own use, so the employer carries the provider's duties as well as the user's: quality management, "
        "technical documentation, conformity assessment and registration (Art. 3(3) and 16). It is the heaviest single "
        "item in the register.")
    add(f"- **One duty already applies to every system in use.** AI literacy for the staff who use {obl['O01']} systems "
        "(Art. 4, since February 2025, now worded as measures to take rather than a level to guarantee). Telling people "
        f"they are talking to an AI is the supplier's duty for {plural(obl['O03'], 'system', 'systems')} (Art. 50(1), "
        "since August 2026); the employer checks it is switched on.")
    add(f"- **Telling the workers is already national law, whatever the AI Act's timetable.** In Germany the works "
        f"council has to be informed about {rule['W-DE1']} systems and agree to at least {rule['W-DE2']} before they "
        f"are used; in Spain it is owed the parameters of {rule['W-ES1']}; in Italy "
        f"{plural(rule['W-IT1'], 'fully automated system needs', 'fully automated systems need')} a written notice to "
        f"each worker and the unions, and {plural(rule['W-IT2'], 'monitoring tool needs', 'monitoring tools need')} a "
        f"union agreement; in Poland {plural(rule['W-PL1'], 'monitoring tool needs', 'monitoring tools need')} two "
        "weeks' notice.")
    add("")

    add("## 1. The register")
    add("")
    add(md_table(["System", "HR function", "Class", "Role", "Workers in scope"],
                 [[row.system, systems.loc[row.system_id, "function"], row._3, row.role, f"{row.workers:,}"]
                  for row in r.itertuples()], "lllll"))
    add("")
    add("*Workers in scope: employees of the employers and departments where the system is used. Recruitment systems "
        "also reach applicants, who are not counted. The same register runs on any list of systems in the "
        "[browser tool](https://d0m3n1c0x.github.io/ai-act-hr-readiness-kit/tool/).*")
    add("")
    add("How the class is decided, in this order:")
    add("")
    add("1. **Prohibited** if the system infers emotions at work and is not there for medical or safety reasons "
        "(Art. 5(1)(f)).")
    add("2. **High-risk** if it is used for recruitment or selection (Annex III 4(a)), or for decisions on terms of "
        "work, promotion, termination, allocating tasks based on individual behaviour or personal traits, or monitoring "
        "and evaluating people (4(b)), unless one of the four conditions of Art. 6(3) applies; a system that profiles "
        "people is high-risk in every case.")
    add("3. **Not high-risk under Art. 6(3)** if it is in Annex III but only performs a narrow procedural or "
        "preparatory task, or improves or checks a human decision, without profiling. The provider documents why.")
    add("4. **Transparency only** if it talks to people (Art. 50(1)); otherwise **minimal risk**, with AI literacy "
        "as the one duty.")
    add("")

    add("## 2. What applies, and when")
    add("")
    order = sorted(OBLIGATIONS, key=lambda o: (o[4], o[0]))
    add(md_table(["Obligation", "Article", "From", "Systems", "Status"],
                 [[name, art, day(when), obl[key], "In force" if when <= ASSESSMENT_DATE else "Ahead"]
                  for key, name, art, _c, when, *_ in order], "llrrl"))
    add("")
    add("Considered and not applicable:")
    add("")
    for name, art, why in NOT_APPLICABLE:
        add(f"- **{name}** ({art}). {why}")
    add("")

    add("## 3. Telling the workers, country by country")
    add("")
    add("The AI Act adds its own duty for high-risk systems from December 2027: inform workers' representatives and "
        f"the affected workers before use (Art. 26(7)), for {obl['O08']} systems here. The national rules below "
        "apply now, and they reach further than the AI Act's high-risk list.")
    add("")
    for country in ENTITIES:
        rules = [w for w in WORKER_RULES if w[1] == country]
        add(f"**{ENTITIES[country]}**")
        add("")
        for key, _c, name, src, _cond, what, when in rules:
            hit = list(r.loc[r[key] == "Yes", "system"])
            who = ", ".join(hit) if hit else "no system in this register"
            add(f"- **{name}** ({src}): {who}. {what}; {when[0].lower() + when[1:]}.")
        add("")
    others = [c for c in COUNTRIES if c not in ENTITIES]
    n_other = sum(1 for w in WORKER_RULES if w[1] in others)
    add(f"**{WORDS[len(others)].capitalize()} more countries, for an employer elsewhere.** The register also holds "
        f"{n_other} rules for {', '.join(COUNTRY_NAMES[c] for c in others[:-1])} and {COUNTRY_NAMES[others[-1]]}: "
        "the CSE in France (information before recruitment techniques and automated HR processing are used, "
        "consultation before monitoring), the works council's advice and consent in the Netherlands (void without "
        "consent), consent in Austria (one replaceable by the conciliation board, one not), three months' notice for a "
        "new technology in Belgium, and Ireland's information and consultation forum where one exists. None applies "
        "to this employer; the [browser tool](https://d0m3n1c0x.github.io/ai-act-hr-readiness-kit/tool/) runs them "
        "on any list of systems.")
    add("")
    add("The [worker information pack](../docs/worker-information.md) has, for each country, who to tell, what the "
        "notice must contain and a model text.")
    add("")

    q, lit = s["questions"], s["literacy"]
    vendor_high = int(((r["class"] == HIGH_RISK) & (r["system_id"].map(systems["supplier"]) == "Vendor")).sum())
    add("## 4. What to ask each supplier")
    add("")
    add(f"Most deployer duties can only be met with facts the supplier holds. The register turns them into "
        f"{len(VENDOR_QUESTIONS)} questions and sends each system's supplier the ones its class calls for: "
        f"{sum(q.values())} in all, most of them for the {vendor_high} bought high-risk systems. In-house systems are "
        "asked of the team that built them.")
    add("")
    add(md_table(["Question", "Article", "Systems"],
                 [[question, art, q[key]] for key, question, art, _c, _w in VENDOR_QUESTIONS], "llr"))
    add("")
    add("The [supplier questionnaire](../deliverables/supplier_questionnaire.md) lists them system by system, ready to "
        "send.")
    add("")

    add("## 5. AI literacy: who learns what")
    add("")
    add("Since the Digital Omnibus, Article 4 asks providers and deployers to *take measures to support* the AI literacy "
        "of the people who operate and use their systems, taking into account their knowledge and the context, without "
        "guaranteeing any level. The register maps each system to the modules its answers call for:")
    add("")
    add(md_table(["Module", "For whom", "Systems"], [[m, who, lit[key]] for key, m, who, _c, _w in LITERACY], "llr"))
    add("")
    add(f"Evidence to keep: {LITERACY_EVIDENCE[0].lower() + LITERACY_EVIDENCE[1:]}. The "
        "[literacy plan](../deliverables/ai_literacy_plan.md) gives the modules per system.")
    add("")

    add("## 6. The fundamental rights impact assessment")
    add("")
    n_high = s["n_" + HIGH_RISK]
    add(f"**Not owed here, drafted anyway.** Article 27 asks for the assessment before the first use of a high-risk "
        f"system by bodies governed by public law and private entities providing public services (and by deployers of "
        f"credit and life and health insurance systems, which no HR system is). The deployer here is a "
        f"{DEPLOYER.lower()}, so obligation O14 is off; the kit still drafts the assessment for its {n_high} high-risk "
        "systems, because the questions it asks are the ones a works council, a data protection authority or a court "
        "will ask, and because a public employer running the tool will owe it.")
    add("")
    add("Since Regulation 2026/1744 the assessment may cross-refer to the data protection impact assessment where that "
        "already covers an element (Art. 27(4) as replaced). The six elements, and the section of a GDPR Article 35(7) "
        "assessment that usually holds each:")
    add("")
    add(md_table(["Art. 27(1)", "Element", "DPIA (Art. 35(7))", "In the kit"],
                 [[k, e, d, x] for k, e, d, x in FRIA_ELEMENTS], "llll"))
    add("")
    add("A public body also registers its use of each high-risk system in the EU database and may not use one the "
        "provider has not registered (Art. 26(8), 49(3)), and its legacy systems comply by 2 August 2030 whatever their "
        "design changes (Art. 111(2)). The [draft assessments](../deliverables/fria_drafts.md) are pre-filled from the "
        "register, one per high-risk system.")
    add("")

    add("## 7. The judgement calls")
    add("")
    add("- **Shift scheduling is a boundary case.** On availability and certified skills alone it might not evaluate "
        "anyone; past attendance makes it allocate tasks on individual behaviour, which is profiling. The register "
        "classifies it as high-risk, and a supplier that drops attendance from the inputs would change the answer.")
    add("- **The interview scheduler is not high-risk, on the provider's word.** It performs a narrow procedural task "
        "(Art. 6(3)(a)), but the documented assessment is the provider's to make (Art. 6(4)); the employer should hold "
        "a copy, and revisit it if the tool starts ranking candidates.")
    add("- **The pay review recommender sits under two laws.** It is high-risk under the AI Act (Annex III 4(b)), and "
        "its pay-setting criteria must be objective and gender-neutral under the Pay Transparency Directive (Art. 4(4) "
        "and 6(1)), whose "
        "categories and 5% screen are in [pay-transparency-readiness-kit](https://github.com/D0M3N1C0X/pay-transparency-readiness-kit).")
    add("- **Learning recommendations stay minimal only while they do not count.** If course completion fed promotion "
        "or pay, the system would move into Annex III 4(b).")
    add("- **The right to an explanation (Art. 86)** is in a chapter that applies from August 2026, but it attaches to "
        "decisions based on high-risk Annex III systems, a classification that applies from December 2027. The "
        "register dates it with the high-risk duties; the reading should be confirmed. It also applies only where "
        "Union law gives no such right already (Art. 86(3)), and GDPR Art. 15(1)(h) and 22 often do.")
    add("- **Systems already in use and Article 111(2).** The grace period follows the type and model, not the "
        "employer's installation (recital 39 of Reg. 2026/1744): a system on the market before 2 December 2027 stays "
        "outside the high-risk duties until its design changes significantly. The register keeps the duties on the "
        "list, because a supplier's next major release, or a retrained in-house model, ends the grace period.")
    add("- **Applicant-only systems and Italy's notice.** Art. 1-bis of D.lgs. 152/1997 informs the worker, so the "
        "register leaves out systems used only on applicants, such as ad targeting; candidates who are hired are told "
        "at hiring. A cautious employer tells them anyway.")
    add("- **Data protection law does not wait for 2027.** A data protection impact assessment is already owed for "
        "high-risk processing of employees' data (GDPR Art. 35); from December 2027 the AI Act adds that it must use "
        "the provider's information (Art. 26(9)). For fully automated systems, GDPR Art. 22 already limits decisions "
        "based solely on automated processing.")
    add("- **Germany's co-determination is the binding constraint now.** A system able to monitor conduct or "
        f"performance needs a works agreement before it is introduced (BetrVG §87(1) Nr. 6); "
        f"{plural(rule['W-DE2'], 'system here processes', 'systems here process')} performance data of workers in "
        "Munich, and courts read \"able to\" broadly enough that a chatbot or assistant logging who used it may need "
        "one too.")
    add("")

    add("- **The new countries' rules are read conservatively.** Whether an HR AI system is a *nouvelle technologie* "
        "(France), an *important* technological facility (Netherlands), a system touching human dignity (Austria) or "
        "an *investment* in a new technology (Belgium) is a judgement; the register assumes yes where the system "
        "monitors or changes work, and names it in the verification register.")
    add("")

    add("## 8. The next 90 days")
    add("")
    add(f"1. **Stop the {lower(banned['system'])} pilot** in Barcelona, delete the scores, and tell the supplier and "
        "the candidates assessed.")
    add(f"2. **Decide the {lower(provider['system'])}'s future**: keep it and build the provider's file, buy a "
        "supplier's equivalent, or narrow it to a team-level view that profiles no one.")
    add("3. **Open the works council agenda in Munich** with the information and co-determination items, and send the "
        "Spanish works council the parameters of the systems that affect work.")
    add("4. **Send the Italian notices** for the fully automated systems and settle the agreement for the monitoring "
        "tool; give the Polish notice two weeks before any new monitoring.")
    add(f"5. **Put AI literacy on record**: run the {sum(lit.values())} module-system pairs of the literacy plan and "
        "keep who took which, when, with what material.")
    add(f"6. **Send the supplier questionnaire**: {sum(q.values())} questions, starting with the instructions for use "
        "and the information the data protection impact assessments need; name an overseer per high-risk system.")
    add("7. **Complete the draft fundamental rights assessments** with the DPO, cross-referring to the DPIAs.")
    add("")

    add("## 9. Method, sources and limits")
    add("")
    add("- **Two engines, one answer.** Every class, role and obligation is computed in Python and again by live "
        "formulas in [the register workbook](../deliverables/ai_act_hr_register.xlsx); its Reconciliation sheet "
        "checks each pair, and CI recalculates the workbook with LibreOffice.")
    add("- **Law read in the original.** The AI Act and the Digital Omnibus in the Official Journal; the Italian, German "
        "and Spanish rules on the official legal databases; the Dutch and Austrian ones through their governments' "
        "open-data services, the French on the Ministry of Labour's official code, the Irish in the Irish Statute Book "
        "and the Belgian agreements on the National Labour Council's site; the Polish ones through secondary sources. "
        "Each statement has its status in [docs/verification.md](../docs/verification.md).")
    add("- **Limits.** Invented systems and answers; the classification follows the text of the Regulation, and "
        "Commission guidelines, harmonised standards or national practice can move boundary cases. Not legal advice.")
    add("")
    path = REPORTS / "ai_act_readiness.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    report_html.build()
    return s


def main() -> None:
    write()
    print("report -> reports/ai_act_readiness.md, reports/index.html")


if __name__ == "__main__":
    main()
