"""
The register: every AI system the HR function uses, classified under the AI Act, with the obligations each one
triggers and the national rules on telling the workers.

Each rule here has a twin formula in the workbook (src/build_workbook.py), written in the same order of tests, and
the Reconciliation sheet checks that the two agree on every cell.
"""
import pandas as pd

from config import (
    CHOICES,
    COUNTRIES,
    DEPARTMENTS,
    DEROGATION,
    HEADCOUNT,
    HIGH_RISK,
    MINIMAL,
    OBLIGATIONS,
    PROHIBITED,
    SYSTEMS,
    TRANSPARENCY,
    WORKER_RULES,
)

YES = "Yes"
YES_NO = ["in_it", "in_pl", "in_de", "in_es", "applicants", "infers_emotions", "medical_or_safety", "profiling",
          "interacts", "decides_about_people", "fully_automated", "monitors_workers", "controls_input_data",
          "on_market_before"]


def validate(systems: pd.DataFrame) -> pd.DataFrame:
    """Every answer must be one of its allowed values, spelled as here: Excel compares text without regard to case
    and Python does not, so anything else would let the two engines disagree."""
    allowed = {**{c: {"Yes", "No"} for c in YES_NO}, **{c: set(v) for c, v in CHOICES.items()},
               "scope": {"All", *DEPARTMENTS}}
    bad = [f"{r['system_id']} {c}={r[c]!r}" for r in systems.to_dict("records") for c, ok in allowed.items()
           if r[c] not in ok]
    if bad:
        raise ValueError(f"answers outside the allowed values: {', '.join(bad[:10])}")
    return systems


def load() -> pd.DataFrame:
    # "None" is a value here (no Annex III area, no Article 6(3) condition), not a missing cell
    return validate(pd.read_csv(SYSTEMS, dtype=str, keep_default_na=False))


def headcount() -> pd.DataFrame:
    hc = pd.read_csv(HEADCOUNT)
    return hc[hc["country"].isin(COUNTRIES)].reset_index(drop=True)


def classify(s: dict) -> str:
    """Article 5(1)(f), then Article 6(2)-(3) with Annex III point 4, then Article 50."""
    if s["infers_emotions"] == YES and s["medical_or_safety"] != YES:
        return PROHIBITED
    if s["annex_iii"] != "None":
        # Article 6(3), last subparagraph: a system that profiles people is always high-risk
        if s["profiling"] == YES:
            return HIGH_RISK
        return DEROGATION if s["art6_3_condition"] != "None" else HIGH_RISK
    return TRANSPARENCY if s["interacts"] == YES else MINIMAL


def role(s: dict, cls: str) -> str:
    """Article 3(3) and (11): an employer that puts a high-risk system into service for its own use is its provider."""
    return "Provider and deployer" if s["supplier"] == "In-house" and cls == HIGH_RISK else "Deployer"


def timing(s: dict, cls: str) -> str:
    """Article 111(2) as amended by Reg. 2026/1744: a high-risk system whose type and model was on the market or in
    service before 2 December 2027 falls under the Regulation only once its design changes significantly."""
    if cls != HIGH_RISK:
        return ""
    return "At its next significant design change" if s["on_market_before"] == YES else "From 2 December 2027"


def workers(s: dict, hc: pd.DataFrame) -> int:
    """Employees in the system's scope: its countries, and its department or everyone."""
    inside = hc["country"].map(lambda c: s[f"in_{c.lower()}"] == YES)
    dept = hc["department"] == s["scope"] if s["scope"] != "All" else True
    return int(hc.loc[inside & dept, "workers"].sum())


def applies(condition: str, s: dict, cls: str) -> bool:
    """When an obligation applies to a system. The same tests, in the same order, as the workbook formulas."""
    high = cls == HIGH_RISK
    return {
        "in use": cls != PROHIBITED,
        "prohibited": cls == PROHIBITED,
        "interacts": s["interacts"] == YES and cls != PROHIBITED,
        "high-risk": high,
        "high-risk and input": high and s["controls_input_data"] == YES,
        "high-risk at work": high and s["applicants"] != YES,
        "high-risk and decides": high and s["decides_about_people"] == YES,
        "high-risk in-house": high and s["supplier"] == "In-house",
        "derogation": cls == DEROGATION,
    }[condition]


def triggers(condition: str, country: str, s: dict, cls: str) -> bool:
    """When a national rule on telling the workers applies to a system in a country."""
    if s[f"in_{country.lower()}"] != YES or cls == PROHIBITED:
        return False
    staff = s["applicants"] != YES                                  # used on employees, not only on candidates
    high = cls == HIGH_RISK
    return {
        # art. 1-bis informs the worker: systems used only on applicants are left out (see docs/method.md)
        "fully automated": staff and s["fully_automated"] == YES and (high or s["monitors_workers"] == YES),
        "monitors": s["monitors_workers"] == YES,
        "in the country": True,
        "processes performance": s["monitors_workers"] == YES or (staff and high),
        "selects": s["annex_iii"] == "4(a)" and s["profiling"] == YES and s["decides_about_people"] == YES,
        "affects work": high,
    }[condition]


def build() -> pd.DataFrame:
    """One row per system: its class, role, workers in scope, and a Yes/blank per obligation and national rule."""
    systems, hc = load(), headcount()
    rows = []
    for s in systems.to_dict("records"):
        cls = classify(s)
        row = {"system_id": s["system_id"], "system": s["system"], "class": cls, "role": role(s, cls),
               "timing": timing(s, cls), "workers": workers(s, hc)}
        for key, _name, _art, cond, *_ in OBLIGATIONS:
            row[key] = YES if applies(cond, s, cls) else ""
        for key, country, _name, _src, cond, *_ in WORKER_RULES:
            row[key] = YES if triggers(cond, country, s, cls) else ""
        rows.append(row)
    return pd.DataFrame(rows)


def summary(r: pd.DataFrame) -> dict:
    """The figures the report, the workbook's Summary sheet and the README quote."""
    high = r[r["class"] == HIGH_RISK]
    return {
        "systems": len(r),
        **{f"n_{c}": int((r["class"] == c).sum()) for c in [PROHIBITED, HIGH_RISK, DEROGATION, TRANSPARENCY, MINIMAL]},
        "provider": int((r["role"] == "Provider and deployer").sum()),
        "legacy": int((r["timing"] == "At its next significant design change").sum()),
        # the largest scope of any one high-risk system: the most workers a single system touches
        "max_workers_high": int(high["workers"].max()) if len(high) else 0,
        "workers_total": int(headcount()["workers"].sum()),
        "obligations": {key: int((r[key] == YES).sum()) for key, *_ in OBLIGATIONS},
        "worker_rules": {key: int((r[key] == YES).sum()) for key, *_ in WORKER_RULES},
        "countries": COUNTRIES,
    }
