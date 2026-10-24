"""The classification, obligations and national rules on hand-made cases, and the register's own data."""
import pandas as pd
import pytest

import register
from config import DEROGATION, HIGH_RISK, MINIMAL, PROHIBITED, TRANSPARENCY

BASE = {"system_id": "X", "system": "Test", "function": "", "supplier": "Vendor", "scope": "All", "in_it": "Yes",
        "in_pl": "No", "in_de": "Yes", "in_es": "No", "applicants": "No", "infers_emotions": "No",
        "medical_or_safety": "No", "annex_iii": "None", "profiling": "No", "art6_3_condition": "None",
        "interacts": "No", "decides_about_people": "No", "fully_automated": "No", "monitors_workers": "No",
        "controls_input_data": "No", "rationale": ""}


def s(**kw):
    return {**BASE, **kw}


def test_emotion_recognition_is_prohibited_unless_for_medical_or_safety_reasons():
    assert register.classify(s(infers_emotions="Yes")) == PROHIBITED
    assert register.classify(s(infers_emotions="Yes", medical_or_safety="Yes")) == MINIMAL


def test_profiling_closes_the_article_6_3_door():
    assert register.classify(s(annex_iii="4(b)", art6_3_condition="(a)")) == DEROGATION
    assert register.classify(s(annex_iii="4(b)", art6_3_condition="(a)", profiling="Yes")) == HIGH_RISK
    assert register.classify(s(annex_iii="4(a)")) == HIGH_RISK


def test_outside_annex_iii_only_talking_to_people_matters():
    assert register.classify(s(interacts="Yes")) == TRANSPARENCY
    assert register.classify(s()) == MINIMAL


def test_building_a_high_risk_system_makes_the_employer_its_provider():
    assert register.role(s(supplier="In-house"), HIGH_RISK) == "Provider and deployer"
    assert register.role(s(supplier="In-house"), MINIMAL) == "Deployer"


def test_a_prohibited_system_is_stopped_not_notified():
    x = s(infers_emotions="Yes", monitors_workers="Yes", annex_iii="4(b)")
    cls = register.classify(x)
    assert register.applies("prohibited", x, cls) and not register.applies("in use", x, cls)
    assert not any(register.triggers(c, "DE", x, cls) for c in ("monitors", "used on workers", "processes performance"))


def test_national_rules_need_the_country():
    x = s(monitors_workers="Yes")
    assert register.triggers("monitors", "IT", x, MINIMAL)
    assert not register.triggers("monitors", "PL", x, MINIMAL)


def test_workers_in_scope_follow_country_and_department():
    hc = register.headcount()
    x = s(scope="Customer Service", in_it="Yes", in_de="No")
    expected = int(hc[(hc["country"] == "IT") & (hc["department"] == "Customer Service")]["workers"].sum())
    assert register.workers(x, hc) == expected


def test_the_register_data_uses_only_allowed_values():
    d = register.load()
    yes_no = [c for c in d.columns if c.startswith(("in_", "applicants", "infers", "medical", "profiling", "interacts",
                                                     "decides", "fully", "monitors", "controls"))]
    assert set(d[yes_no].to_numpy().ravel()) <= {"Yes", "No"}
    assert set(d["annex_iii"]) <= {"None", "4(a)", "4(b)"}
    assert set(d["art6_3_condition"]) <= {"None", "(a)", "(b)", "(c)", "(d)"}
    assert set(d["supplier"]) <= {"Vendor", "In-house"}
    assert d["system_id"].is_unique and (d["rationale"].str.len() > 80).all()


def test_headcount_is_the_pay_transparency_organisation():
    assert register.headcount()["workers"].sum() == 3443


@pytest.mark.parametrize("sid,cls", [("S03", PROHIBITED), ("S04", DEROGATION), ("S07", HIGH_RISK),
                                     ("S09", TRANSPARENCY), ("S10", MINIMAL)])
def test_the_headline_cases(sid, cls):
    r = register.build().set_index("system_id")
    assert r.loc[sid, "class"] == cls
    assert isinstance(r, pd.DataFrame)
