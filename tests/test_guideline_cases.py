"""The Commission's examples on emotion recognition, and the fragility of each class."""
import guideline_cases as G
import register


def test_every_case_has_a_paragraph_and_a_verdict():
    c = G.load()
    assert len(c) == 21 and c["case_id"].is_unique
    assert set(c["verdict"]) == {"Prohibited", "Not prohibited"}
    assert c["paragraph"].between(240, 270).all()


def test_the_reworded_questions_agree_with_every_case():
    assert G.evaluate()["new_agrees"].all()


def test_the_first_wording_got_eight_wrong_both_ways():
    e = G.evaluate()
    wrong = e[~e["old_agrees"]]
    assert len(wrong) == 8
    assert (wrong["old_verdict"] == "Prohibited").sum() == 4


def test_text_customers_and_training_are_not_prohibited():
    e = G.evaluate().set_index("case_id")
    for case in ("G05", "G08", "G09", "G14"):
        assert e.loc[case, "new_verdict"] == "Not prohibited"


def test_wellbeing_and_property_are_not_medical_or_safety():
    e = G.evaluate().set_index("case_id")
    for case in ("G15", "G17", "G18", "G20"):
        assert e.loc[case, "new_verdict"] == "Prohibited"


def test_fragility_finds_the_derogation():
    f = G.fragility().set_index("system_id")
    derog = f[f["class"] == register.DEROGATION]
    assert len(derog) == 1
    assert {"annex_iii", "art6_3_condition", "profiling"} <= set(derog.iloc[0]["answers"])
    high = f[f["class"] == register.HIGH_RISK]
    assert all(set(a) == {"annex_iii", "infers_emotions"} for a in high["answers"])
