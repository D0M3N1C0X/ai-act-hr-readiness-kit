"""
Writes what the browser tool needs (web/inputs.json and web/template_ai_systems.csv) and the cases its JavaScript is
checked against (tests/fixtures/js_vectors.json): the twelve systems of the register and random systems covering
every combination of answers, each with the result computed here. tests/js/check_engine.mjs recomputes every case
with web/engine.js and fails at the first difference, so the page and the register cannot drift apart.
"""
import json
import random

import register
from config import (
    ASSESSMENT_DATE,
    CLASSES,
    COUNTRIES,
    D_ANNEX_III,
    D_CHAPTERS_I_II,
    D_GENERAL,
    DEPARTMENTS,
    ENTITIES,
    NOT_APPLICABLE,
    OBLIGATIONS,
    ROOT,
    SYSTEMS,
    WORKER_RULES,
)

WEB = ROOT / "web"
VECTORS = ROOT / "tests" / "fixtures" / "js_vectors.json"
ANSWERS = ["supplier", "scope", "in_it", "in_pl", "in_de", "in_es", "applicants", "infers_emotions",
           "medical_or_safety", "annex_iii", "profiling", "art6_3_condition", "interacts", "decides_about_people",
           "fully_automated", "monitors_workers", "controls_input_data"]
CHOICES = {"supplier": ["Vendor", "In-house"], "scope": ["All", *DEPARTMENTS], "annex_iii": ["None", "4(a)", "4(b)"],
           "art6_3_condition": ["None", "(a)", "(b)", "(c)", "(d)"]}


def cfg() -> dict:
    return {
        "assessment": ASSESSMENT_DATE.isoformat(),
        "dates": {"chapters_i_ii": D_CHAPTERS_I_II.isoformat(), "general": D_GENERAL.isoformat(),
                  "annex_iii": D_ANNEX_III.isoformat()},
        "classes": CLASSES, "countries": COUNTRIES, "entities": ENTITIES, "departments": DEPARTMENTS,
        "headcount": register.headcount().to_dict("records"),
        "obligations": [{"key": k, "name": n, "article": a, "when": c, "from": d.isoformat(), "who": w, "evidence": e}
                        for k, n, a, c, d, w, e in OBLIGATIONS],
        "worker_rules": [{"key": k, "country": c, "name": n, "source": s, "when": w, "what": what, "timing": t}
                         for k, c, n, s, w, what, t in WORKER_RULES],
        "not_applicable": [{"name": n, "article": a, "why": y} for n, a, y in NOT_APPLICABLE],
        "choices": CHOICES,
    }


def expected(s: dict, hc) -> dict:
    cls = register.classify(s)
    return {"class": cls, "role": register.role(s, cls), "workers": register.workers(s, hc),
            "obligations": [k for k, _n, _a, c, *_ in OBLIGATIONS if register.applies(c, s, cls)],
            "rules": [k for k, country, _n, _s, c, *_ in WORKER_RULES if register.triggers(c, country, s, cls)]}


def write_vectors(n: int = 2000, seed: int = 11) -> int:
    hc = register.headcount()
    systems = register.load().to_dict("records")
    rng = random.Random(seed)
    for i in range(n):
        s = {"system_id": f"R{i:04d}", "system": f"Random {i}"}
        for a in ANSWERS:
            s[a] = rng.choice(CHOICES.get(a, ["Yes", "No"]))
        systems.append(s)
    cases = [{"system": {a: s[a] for a in ["system_id", *ANSWERS]}, **expected(s, hc)} for s in systems]
    VECTORS.parent.mkdir(exist_ok=True)
    VECTORS.write_text(json.dumps({"cfg": cfg(), "cases": cases}, ensure_ascii=False, separators=(",", ":")) + "\n",
                       encoding="utf-8")
    return len(cases)


def write_inputs() -> None:
    WEB.mkdir(exist_ok=True)
    (WEB / "inputs.json").write_text(json.dumps(cfg(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = SYSTEMS.read_text(encoding="utf-8").splitlines()
    (WEB / "template_ai_systems.csv").write_text("\n".join(lines[:3]) + "\n", encoding="utf-8")
    (WEB / "ai_systems.csv").write_text(SYSTEMS.read_text(encoding="utf-8"), encoding="utf-8")


def main() -> None:
    write_inputs()
    print(f"tool -> web/inputs.json; {write_vectors()} cases -> tests/fixtures/js_vectors.json")


if __name__ == "__main__":
    main()
