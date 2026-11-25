"""The pay review recommender on the pay-transparency kit's payroll."""
import pytest

import pay_review as P


@pytest.fixture(scope="module")
def sim():
    return P.simulate()


def test_before_the_review_it_is_the_kits_own_figures(sim):
    b = sim["before"]
    assert round(b["group_gap"] * 100, 1) == 17.6
    assert len(b["flags"]) == 12 and len(b["categories"]) == 28


def test_every_design_spends_the_same_budget(sim):
    for d in P.DESIGNS:
        assert sim[d]["spent"] == pytest.approx(P.BUDGET, rel=1e-9)


def test_merit_designs_barely_move_the_gap(sim):
    for d in P.DESIGNS[:3]:
        assert abs(sim[d]["group_gap"] - sim["before"]["group_gap"]) < 0.002


def test_the_equity_fund_clears_every_flag_it_targets(sim):
    eq = sim["Matrix with an equity fund"]
    assert set(eq["cleared"]) == set(sim["before"]["flags"])
    assert eq["group_gap"] < sim["before"]["group_gap"] - 0.015
    assert sim["equity_eur"] < sim["budget_eur"]


def test_the_vendored_files_are_pinned():
    P.verify()
