"""
Writes the three working documents the register feeds, in deliverables/:

- supplier_questionnaire.md: the questions to send each system's supplier, system by system;
- ai_literacy_plan.md: the AI literacy modules each system calls for, and for whom;
- fria_drafts.md: a fundamental rights impact assessment drafted for every high-risk system, pre-filled from the
  register and cross-referred to the data protection impact assessment (Art. 27(4) as replaced by Reg. 2026/1744).

Every Yes comes from src/register.py, the same functions the workbook is reconciled against; the text around it is
written once here. The drafts are starting points for the DPO and HR, not finished assessments.
"""
import register
from config import (
    COUNTRY_NAMES,
    DELIVERABLES,
    DEPARTMENTS,
    DEPLOYER,
    FRIA_ELEMENTS,
    HIGH_RISK,
    LITERACY,
    LITERACY_EVIDENCE,
    PRIVATE,
    VENDOR_QUESTIONS,
    WORKER_RULES,
)

YES = "Yes"
NOTE = ("> Generated from the register by `src/build_deliverables.py`; change the answers in `data/ai_systems.csv` "
        "and run `python src/run_all.py`. A dry run on invented systems, not legal advice.")


def where(s: dict) -> str:
    names = [COUNTRY_NAMES[c] for c in COUNTRY_NAMES if s[f"in_{c.lower()}"] == YES]
    return ", ".join(names[:-1]) + (" and " if len(names) > 1 else "") + names[-1] if names else "no country listed"


def people(s: dict, n: int) -> str:
    dept = "all departments" if s["scope"] == "All" else f"the {s['scope']} department"
    if s["applicants"] == YES:
        return f"Applicants for roles in {where(s)}, in {dept}; candidates who are hired become employees"
    return f"Employees of {dept} in {where(s)}: {n:,} workers in this register's headcount"


def risks(s: dict) -> list[str]:
    out = []
    if s["annex_iii"] == "4(a)":
        out.append("Unequal access to employment: a ranking or filter that reproduces past hiring patterns, or uses "
                   "proxies for sex, age, disability or origin")
    if s["annex_iii"] == "4(b)":
        out.append("Unequal treatment in pay, promotion, task allocation or dismissal, including pay criteria that are "
                   "not gender-neutral")
    if s["profiling"] == YES:
        out.append("Profiling: people scored on predicted behaviour they cannot see or contest")
    if s["monitors_workers"] == YES:
        out.append("Privacy and dignity at work, and a chilling effect on how people work")
    if s["fully_automated"] == YES:
        out.append("Results that take effect with no person checking each one, where GDPR Art. 22 limits decisions "
                   "based solely on automated processing")
    if s["decides_about_people"] == YES:
        out.append("Decisions people cannot have explained or reviewed")
    out.append("Errors and drift: accuracy lower for some groups than the provider's headline figure (ask V02-V03)")
    return out


def supplier_questionnaire(r, systems) -> str:
    L = ["# Questions for the supplier", "", NOTE, "",
         "What the employer can only do with the supplier's help, system by system: the instructions for use, the "
         "facts behind the notices to workers and the data protection impact assessment, the logs, and the warning "
         "before a design change that would end the grace period of Article 111(2). Send before signing or at "
         "renewal; keep the answers with the register.", ""]
    q = {k: (question, art, why) for k, question, art, _c, why in VENDOR_QUESTIONS}
    for row in r.itertuples():
        s = systems.loc[row.system_id]
        keys = [k for k in q if r.loc[r["system_id"] == row.system_id, k].iloc[0] == YES]
        L.append(f"## {row.system_id} · {row.system}")
        L.append("")
        if s["supplier"] != "Vendor":
            L.append(f"*{row._3}, built in-house: the team that built it answers these as the provider would.*")
            L.append("")
            continue
        L.append(f"*{row._3}. {len(keys)} questions.*")
        L.append("")
        for i, k in enumerate(keys, start=1):
            question, art, why = q[k]
            L.append(f"{i}. **{question}** ({art}). {why}.")
        L.append("")
    return "\n".join(L) + "\n"


def literacy_plan(r) -> str:
    L = ["# AI literacy plan", "", NOTE, "",
         "Article 4, as replaced by Regulation (EU) 2026/1744, asks providers and deployers to take measures to support "
         "the AI literacy of their staff and of others who operate and use AI systems on their behalf, taking into "
         "account their technical knowledge, experience, education and training, the context of use, and the people "
         "the systems are used on. It does not require any level to be guaranteed.", "",
         f"**Evidence to keep:** {LITERACY_EVIDENCE}.", "", "## Modules", ""]
    for key, module, who, _cond, covers in LITERACY:
        hit = list(r.loc[r[key] == YES, "system"])
        L.append(f"### {key} · {module}")
        L.append("")
        L.append(f"- **For:** {who}")
        L.append(f"- **Covers:** {covers}")
        L.append(f"- **Systems ({len(hit)}):** {', '.join(hit) if hit else 'none in this register'}")
        L.append("")
    L += ["## By system", "", "| System | Class | Modules |", "|---|---|---|"]
    for row in r.itertuples():
        mods = [k for k, *_ in LITERACY if r.loc[r["system_id"] == row.system_id, k].iloc[0] == YES]
        L.append(f"| {row.system} | {row._3} | {', '.join(mods) if mods else 'none: the system is stopped'} |")
    return "\n".join(L) + "\n"


def fria_drafts(r, systems) -> str:
    owed = DEPLOYER != PRIVATE
    L = ["# Fundamental rights impact assessments: drafts", "", NOTE, "",
         f"**Status for this deployer ({DEPLOYER.lower()}):** "
         + ("owed before the first use of each high-risk system (Art. 27(1)), with the results notified to the market "
            "surveillance authority on the AI Office template (Art. 27(3), (5))." if owed else
            "not owed. Article 27(1) applies to bodies governed by public law, private entities providing public "
            "services, and deployers of credit and life and health insurance systems. These drafts are voluntary: "
            "they ask the questions a works council, a data protection authority or a court will ask, and they turn "
            "into the real assessment if the deployer changes."), "",
         "Each draft follows the six elements of Article 27(1). Where the data protection impact assessment already "
         "meets an element, the assessment may cross-refer to it or include the relevant part (Art. 27(4) as replaced "
         "by Regulation (EU) 2026/1744); the third column names the section of a GDPR Article 35(7) assessment that "
         "usually holds it. Text in brackets is for the employer to complete.", ""]
    rules = {k: (c, name) for k, c, name, *_ in WORKER_RULES}
    for row in r[r["class"] == HIGH_RISK].itertuples():
        s = systems.loc[row.system_id]
        told = [f"{k} ({COUNTRY_NAMES[rules[k][0]]})" for k in rules
                if r.loc[r["system_id"] == row.system_id, k].iloc[0] == YES]
        decides = s["decides_about_people"] == YES
        draft = {
            "(a)": f"{s['function']}. {s['rationale'].split('. ')[0].rstrip('.')}.",
            "(b)": "[In use since or from: date; for how long: until the contract ends or a set review date; how often "
                   "it runs: on every application, every rota, every review cycle.]",
            "(c)": people(s, row.workers) + ". [Groups to look at: women, older workers, people with disabilities, "
                   "workers of foreign origin, part-time workers.]",
            "(d)": "; ".join(x if i == 0 else x[0].lower() + x[1:] for i, x in enumerate(risks(s))) + ".",
            "(e)": "[Named overseer and deputy] with the competence, training and authority to override or stop it "
                   "(Art. 26(2)); the oversight measures of the instructions for use (supplier answer V04); "
                   "literacy module L02.",
            "(f)": "Suspend and tell the provider if it presents a risk; report serious incidents (Art. 26(5)). "
                   "Complaints to [channel], answered within [time]"
                   + ("; an explanation of the system's role on request (Art. 86)" if decides else "")
                   + (f"; workers' representatives involved under {', '.join(told)}" if told else "") + ".",
        }
        L.append(f"## {row.system_id} · {row.system}")
        L.append("")
        L.append(f"*{s['supplier']}; {row.role.lower()}; high-risk duties: {row.timing.lower()}.*")
        L.append("")
        L.append("| Art. 27(1) | Draft | DPIA (Art. 35(7)) |")
        L.append("|---|---|---|")
        for key, element, dpia, _kit in FRIA_ELEMENTS:
            L.append(f"| **{key}** {element} | {draft[key]} | {dpia} |")
        L.append("")
    return "\n".join(L) + "\n"


def write() -> list[str]:
    systems = register.load().set_index("system_id")
    r = register.build()
    assert set(systems["scope"]) <= {"All", *DEPARTMENTS}
    out = {"supplier_questionnaire.md": supplier_questionnaire(r, systems),
           "ai_literacy_plan.md": literacy_plan(r),
           "fria_drafts.md": fria_drafts(r, systems)}
    DELIVERABLES.mkdir(exist_ok=True)
    for name, text in out.items():
        (DELIVERABLES / name).write_text(text, encoding="utf-8")
    return list(out)


def main() -> None:
    print(f"deliverables -> {', '.join('deliverables/' + n for n in write())}")


if __name__ == "__main__":
    main()
