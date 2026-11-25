"""The provider's file for the in-house attrition model, and its agreement with hr-people-analytics."""
import hashlib

import provider_file as P


def test_the_vendored_card_is_the_pinned_one():
    assert hashlib.sha256(P.CARD.read_bytes()).hexdigest() == P.CARD_SHA256


def test_every_duty_has_an_article_and_a_known_status():
    f = P.load()
    assert f["ref"].is_unique and len(f) == 21
    assert (f["article"].str.startswith("Art.")).all()
    assert set(f["status"]) <= set(P.STATUSES)
    # a duty not fully covered says what is missing, except where the duty itself is the whole gap
    assert (f.loc[f["status"] == "Partly", "gap"] != "").all()


def test_the_card_and_the_register_agree():
    c = P.consistency()
    assert c["class_agrees"] and c["role_agrees"]
    assert c["unanswered"] == []
    assert len(c["asked"]) == 14


def test_the_counts_hold():
    assert P.summary()["counts"] == {"Covered": 3, "Partly": 10, "Missing": 8}
