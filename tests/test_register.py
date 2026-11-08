"""The classification, obligations and national rules on hand-made cases, and the register's own data."""
import pandas as pd
import pytest

import register
from config import DEROGATION, HIGH_RISK, MINIMAL, PROHIBITED, TRANSPARENCY

BASE = {"system_id": "X", "system": "Test", "function": "", "supplier": "Vendor", "scope": "All", "in_it": "Yes",
        "in_pl": "No", "in_de": "Yes", "in_es": "No", "in_fr": "No", "in_nl": "No", "in_ie": "No",
        "in_at": "No", "in_be": "No", "applicants": "No", "infers_emotions": "No",
        "medical_or_safety": "No", "annex_iii": "None", "profiling": "No", "art6_3_condition": "None",
        "interacts": "No", "decides_about_people": "No", "fully_automated": "No", "monitors_workers": "No",
        "controls_input_data": "No", "on_market_before": "Yes", "rationale": ""}


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


def test_a_profiling_system_with_a_6_3_condition_still_triggers_the_national_rules():
    # high-risk through profiling: the rules that follow the class must follow it too (review of 24 October 2026)
    x = s(annex_iii="4(b)", profiling="Yes", art6_3_condition="(a)", in_es="Yes", fully_automated="Yes")
    cls = register.classify(x)
    assert cls == HIGH_RISK
    assert register.triggers("affects work", "ES", x, cls)
    assert register.triggers("fully automated", "IT", x, cls)
    assert register.triggers("processes performance", "DE", x, cls)


def test_systems_already_on_the_market_wait_for_a_significant_change():
    x = s(annex_iii="4(a)", profiling="Yes")
    assert register.timing({**x, "on_market_before": "Yes"}, HIGH_RISK) == "At its next significant design change"
    assert register.timing({**x, "on_market_before": "No"}, HIGH_RISK) == "From 2 December 2027"
    assert register.timing(x, MINIMAL) == ""


def test_italy_notice_is_for_workers_not_applicants():
    x = s(annex_iii="4(a)", profiling="Yes", applicants="Yes", fully_automated="Yes")
    assert not register.triggers("fully automated", "IT", x, register.classify(x))


def test_answers_must_be_spelled_as_allowed():
    d = register.load()
    bad = d.copy()
    bad.loc[0, "infers_emotions"] = "yes"          # Excel would read this as Yes, Python would not
    with pytest.raises(ValueError):
        register.validate(bad)


def test_a_private_employer_owes_no_fria_a_public_one_does():
    x = s(annex_iii="4(a)", profiling="Yes")
    cls = register.classify(x)
    assert not register.applies("high-risk and public", x, cls, "Private employer")
    assert register.applies("high-risk and public", x, cls, "Private entity providing public services")
    assert register.applies("high-risk and public body", x, cls, "Public body")
    assert not register.applies("high-risk and public body", x, cls, "Private entity providing public services")


def test_public_bodies_get_a_long_stop_date_for_legacy_systems():
    x = s(annex_iii="4(a)", profiling="Yes")
    assert register.timing(x, HIGH_RISK, "Public body") == register.LEGACY_PUBLIC
    assert register.timing(x, HIGH_RISK, "Private entity providing public services") == register.LEGACY
    assert register.timing({**x, "on_market_before": "No"}, HIGH_RISK, "Public body") == "From 2 December 2027"


def test_new_countries_need_the_country_and_follow_their_conditions():
    x = s(in_fr="Yes", in_nl="Yes", in_at="Yes", in_be="Yes", in_ie="Yes", monitors_workers="Yes")
    cls = register.classify(x)
    for country, cond in (("FR", "monitors"), ("AT", "monitors"), ("BE", "monitors"), ("NL", "on employees"),
                          ("IE", "changes work organisation"), ("BE", "changes work organisation")):
        assert register.triggers(cond, country, x, cls), (country, cond)
    assert not register.triggers("monitors", "FR", {**x, "in_fr": "No"}, cls)
    applicants_only = s(in_nl="Yes", in_at="Yes", applicants="Yes")
    assert not register.triggers("on employees", "NL", applicants_only, MINIMAL)
    assert not register.triggers("on employees", "AT", applicants_only, MINIMAL)


def test_questions_go_to_vendors_only():
    x = s(annex_iii="4(a)", profiling="Yes")
    assert register.asks("high-risk", x, HIGH_RISK)
    assert not register.asks("high-risk", {**x, "supplier": "In-house"}, HIGH_RISK)


def test_every_rule_question_and_module_has_a_known_condition():
    from config import LITERACY, OBLIGATIONS, VENDOR_QUESTIONS, WORKER_RULES
    x = s()
    for _k, _n, _a, cond, *_ in OBLIGATIONS:
        register.applies(cond, x, MINIMAL)
    for _k, country, _n, _s, cond, *_ in WORKER_RULES:
        register.triggers(cond, country, {**x, f"in_{country.lower()}": "Yes"}, MINIMAL)
    for _k, _q, _a, cond, _w in VENDOR_QUESTIONS:
        register.asks(cond, x, MINIMAL)
    for _k, _m, _w, cond, _x in LITERACY:
        register.applies(cond, x, MINIMAL)
