"""
The pay review recommender (S08) under both laws: run on the payroll of pay-transparency-readiness-kit, does it close
the gender pay gaps the Directive makes the employer report, or widen them?

S08 is high-risk under the AI Act (Annex III 4(b)); its criteria must also be objective and gender-neutral under the
Pay Transparency Directive (Art. 4(4), 6(1)), and next year's report will show what it did. The register cannot say
which way it goes; a simulation on the same payroll can. Three designs a supplier might ship, one review budget:

- **Rating only**: the rise follows the performance rating.
- **Merit matrix**: the rise follows the rating and where the person sits in the pay range for their role, so people
  below the middle of the range get more. The usual design.
- **Matrix with a retention boost**: the matrix, plus two points for people the attrition model would flag on its two
  strongest signs, paid below 92% of the range middle or on a fixed-term contract. That is a pay decision taken on a
  predicted intention to leave, the use the model card rules out (V01).
- **Matrix with an equity fund**: first, in every category flagged before the review, the lower-paid sex gets the
  rise that brings its mean hourly pay to the other's (the kit's cost to close, out of the same budget); the rest of
  the budget follows the matrix.

Each design is scaled to the same budget (3% of base pay per employer). The gaps are recomputed with the
pay-transparency kit's rules: hourly pay level with all components, categories from its job evaluation (weights 35,
15, 35, 15 and its point bands), flagged at 5% on hourly or annual pay. The payroll and the grid are vendored at a
pinned checksum; before any rise, the code reproduces the kit's published figures (a 17.6% group gap, 12 of 28
categories flagged).
"""
import hashlib

import numpy as np
import pandas as pd

from config import DATA

PAYROLL = DATA / "source" / "ptk_payroll_extract.csv"
GRID = DATA / "source" / "ptk_job_evaluation.csv"
PTK_REPO = "https://github.com/D0M3N1C0X/pay-transparency-readiness-kit"
PTK_COMMIT = "a086680"
SHA256 = {PAYROLL: "647531fa917a4f746f674e2313533d4b6528570de3eae5a7d821c7db297b6a93",
          GRID: "7c4b4ee03db9481893374b9100c8b4a75c4a44b1688b20f9b726df2874c628b0"}

# The pay-transparency kit's own settings (its src/config.py)
WEIGHTS = {"skills": 35, "effort": 15, "responsibility": 35, "working_conditions": 15}
BANDS = [(100, "Cat A"), (160, "Cat B"), (200, "Cat C"), (250, "Cat D"), (300, "Cat E"), (340, "Cat F"),
         (400, "Cat G")]
THRESHOLD = 0.05
WEEKS = 52
COMPONENTS = ["bonus", "commission", "shift_allowance", "car_allowance"]

BUDGET = 0.03                                   # of base pay, per employer
RATING = {1: 0.0, 2: 0.5, 3: 1.0, 4: 1.5, 5: 2.0}   # relative rise by performance rating
POSITION = [(0.92, 1.5), (1.00, 1.2), (1.08, 1.0), (9.99, 0.6)]  # (compa-ratio up to, multiplier)
BOOST = 0.02                                    # retention boost, points of base pay
FLAG_BELOW = 0.92
DESIGNS = ["Rating only", "Merit matrix", "Matrix with a retention boost", "Matrix with an equity fund"]


def verify() -> None:
    for path, digest in SHA256.items():
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise SystemExit(f"{path} does not match the pinned checksum; "
                             f"copy it again from {PTK_REPO} at {PTK_COMMIT}")


def payroll() -> pd.DataFrame:
    verify()
    w = pd.read_csv(PAYROLL)
    g = pd.read_csv(GRID)
    g["points"] = sum(g[f] * WEIGHTS[f] for f in WEIGHTS)
    g["category"] = g["points"].map(lambda p: [name for floor, name in BANDS if p >= floor][-1])
    w = w.merge(g[["role", "category"]], on="role", validate="many_to_one")
    w["fte_base"] = w["base_pay"] / w["fte"]
    # Compa-ratio against the middle of the role's range in each country, read as the median full-time base pay
    w["compa"] = w["fte_base"] / w.groupby(["country", "role"])["fte_base"].transform("median")
    return w


def equity(w: pd.DataFrame) -> pd.Series:
    """The rise, as a share of base pay, that lifts the lower-paid sex's mean hourly pay to the other's in every
    category flagged before the review: the same uplift for each of them."""
    m = measure(w)
    hourly = (w["base_pay"] + w[COMPONENTS].sum(axis=1)) / (w["weekly_hours"] * WEEKS)
    lift = pd.Series(0.0, index=w.index)
    for c, cat in m["flags"]:
        g = w[(w["country"] == c) & (w["category"] == cat)]
        f, mm = hourly[g.index][g["gender"] == "F"], hourly[g.index][g["gender"] == "M"]
        low = g.index[g["gender"] == ("F" if f.mean() < mm.mean() else "M")]
        diff = abs(mm.mean() - f.mean())                     # euro an hour for each of the lower-paid sex
        lift.loc[low] = diff * w.loc[low, "weekly_hours"] * WEEKS / w.loc[low, "base_pay"]
    return lift


def rises(w: pd.DataFrame, design: str) -> pd.Series:
    """The rise each worker gets, as a share of base pay, scaled to BUDGET of each employer's base pay."""
    weight = w["performance_rating"].map(RATING).astype(float)
    if design != "Rating only":
        mult = np.select([w["compa"] <= cut for cut, _ in POSITION], [m for _, m in POSITION])
        weight = weight * mult
    rise = pd.Series(0.0, index=w.index)
    for _, idx in w.groupby("country").groups.items():
        part, base = weight.loc[idx], w.loc[idx, "base_pay"]
        extra = 0.0
        if design == "Matrix with a retention boost":
            flagged = (w.loc[idx, "compa"] < FLAG_BELOW) | (w.loc[idx, "contract_type"] == "Fixed-term")
            extra = flagged.astype(float) * BOOST
            budget_left = BUDGET * base.sum() - (extra * base).sum()
        elif design == "Matrix with an equity fund":
            extra = equity(w).loc[idx]
            budget_left = max(0.0, BUDGET * base.sum() - (extra * base).sum())
        else:
            budget_left = BUDGET * base.sum()
        scale = budget_left / (part * base).sum() if (part * base).sum() else 0.0
        rise.loc[idx] = part * scale + extra
    return rise


def gap(f: pd.Series, m: pd.Series) -> float:
    return float((m.mean() - f.mean()) / m.mean())


def measure(w: pd.DataFrame, rise: pd.Series | None = None) -> dict:
    """The pay-transparency figures after a review: group gap, gaps by employer, flagged categories."""
    base = w["base_pay"] * (1 + (0 if rise is None else rise))
    total = base + w[COMPONENTS].sum(axis=1)
    hourly = total / (w["weekly_hours"] * WEEKS)
    x = w.assign(total=total, hourly=hourly, base_new=base)
    women, men = x["gender"] == "F", x["gender"] == "M"
    flags, rows = [], []
    for (c, cat), g in x.groupby(["country", "category"]):
        f, m = g[g["gender"] == "F"], g[g["gender"] == "M"]
        if f.empty or m.empty:
            continue
        gh, ga = gap(f["hourly"], m["hourly"]), gap(f["total"], m["total"])
        flagged = abs(gh) >= THRESHOLD or abs(ga) >= THRESHOLD
        rows.append({"country": c, "category": cat, "gap_hourly": gh, "flagged": flagged})
        if flagged:
            flags.append((c, cat))
    return {"group_gap": gap(x.loc[women, "hourly"], x.loc[men, "hourly"]),
            "by_country": {c: gap(g.loc[g["gender"] == "F", "hourly"], g.loc[g["gender"] == "M", "hourly"])
                           for c, g in x.groupby("country")},
            "flags": sorted(flags), "categories": pd.DataFrame(rows),
            "women_share_rise": float((x.loc[women, "base_new"] - w.loc[women, "base_pay"]).sum()
                                      / (x["base_new"] - w["base_pay"]).sum()) if rise is not None else None}


def simulate() -> dict:
    w = payroll()
    before = measure(w)
    out = {"before": before, "workers": len(w), "women_share": float((w["gender"] == "F").mean()),
           "women_share_base": float(w.loc[w["gender"] == "F", "base_pay"].sum() / w["base_pay"].sum())}
    for d in DESIGNS:
        r = rises(w, d)
        after = measure(w, r)
        out[d] = {**after, "mean_rise_f": float(r[w["gender"] == "F"].mean()),
                  "mean_rise_m": float(r[w["gender"] == "M"].mean()),
                  "new_flags": sorted(set(after["flags"]) - set(before["flags"])),
                  "cleared": sorted(set(before["flags"]) - set(after["flags"])),
                  "spent": float((r * w["base_pay"]).sum() / w["base_pay"].sum()),
                  "spent_eur": float((r * w["base_pay"]).sum())}
    out["budget_eur"] = float(BUDGET * w["base_pay"].sum())
    out["equity_eur"] = float((equity(w) * w["base_pay"]).sum())
    return out


if __name__ == "__main__":
    s = simulate()
    b = s["before"]
    print("before", round(b["group_gap"], 4), len(b["flags"]), "of", len(b["categories"]))
    for d in DESIGNS:
        x = s[d]
        print(d, round(x["group_gap"], 4), len(x["flags"]), "new", x["new_flags"], "cleared", x["cleared"],
              "rise f/m", round(x["mean_rise_f"], 4), round(x["mean_rise_m"], 4),
              "women share", round(x["women_share_rise"], 3), "spent", round(x["spent"], 4))
    print("women share of staff", round(s["women_share"], 3), "of base", round(s["women_share_base"], 3))
