"""
The in-house attrition model as a real case: what the provider's file already holds, and what is missing.

S07 is the one system in the register the employer builds itself, so the employer is its provider (Art. 3(3), 16).
hr-people-analytics built that model, validated it out of time, audited it by group and wrote its model card, which
answers the register's supplier questions as the provider. This module sets that evidence against the provider's
duties of Regulation (EU) 2024/1689 (Articles 9 to 20, 43, 47 to 49, 72 and 73), one row per duty in
data/provider_file_s07.csv, and checks the two repositories agree: the card's classification and role must be the
register's, and the supplier questions the card answers must be the ones the register asks of S07.

The model card is vendored at a pinned commit and checksum (data/source/model_card_s07.md), as the headcount is.
"""
import hashlib
import re

import pandas as pd

import register
from config import DATA, VENDOR_QUESTIONS

FILE = DATA / "provider_file_s07.csv"
CARD = DATA / "source" / "model_card_s07.md"
CARD_REPO = "https://github.com/D0M3N1C0X/hr-people-analytics"
CARD_COMMIT = "ab46942"
CARD_SHA256 = "b19c7a90dde7f17eadbe90641181ad34518d3d88897a989b39d2a8f7a45846a3"
STATUSES = ["Covered", "Partly", "Missing"]


def verify_card() -> str:
    text = CARD.read_text(encoding="utf-8")
    digest = hashlib.sha256(CARD.read_bytes()).hexdigest()
    if digest != CARD_SHA256:
        raise SystemExit(f"{CARD} does not match the pinned checksum; copy it again from {CARD_REPO} at {CARD_COMMIT}")
    return text


def load() -> pd.DataFrame:
    f = pd.read_csv(FILE, keep_default_na=False)
    bad = set(f["status"]) - set(STATUSES)
    if bad:
        raise ValueError(f"unknown statuses in {FILE.name}: {bad}")
    return f


def card_facts(text: str) -> dict:
    """What the model card says about itself: its class, its role and the supplier questions it answers."""
    cls = re.search(r"\*\*Classification\*\* \| ([^,|]+)", text).group(1).strip()
    role = re.search(r"\*\*Role\*\* \| ([^:|]+)", text).group(1).strip()
    answered = sorted(set(re.findall(r"^## (V\d{2})\b", text, flags=re.M)))
    return {"class": cls, "role": role, "answered": answered}


def consistency() -> dict:
    """The card against the register: same class, same role, and every question the register asks S07 answered."""
    card = card_facts(verify_card())
    r = register.build()
    s07 = r[r["system_id"] == "S07"].iloc[0]
    answers = register.load().set_index("system_id").loc["S07"].to_dict()
    # In-house, nobody sends S07 the questionnaire; these are the questions its supplier would get if it were bought,
    # which the provider has to answer for itself.
    asked = [key for key, _, _, cond, _ in VENDOR_QUESTIONS if register.applies(cond, answers, s07["class"])]
    return {"card": card, "register_class": s07["class"], "register_role": s07["role"],
            "asked": asked, "unanswered": sorted(set(asked) - set(card["answered"])),
            "class_agrees": card["class"] == s07["class"], "role_agrees": card["role"] == s07["role"]}


def summary() -> dict:
    f = load()
    counts = f["status"].value_counts().reindex(STATUSES, fill_value=0)
    return {"file": f, "counts": counts.to_dict(), "n": len(f), "consistency": consistency()}


if __name__ == "__main__":
    s = summary()
    print(s["counts"])
    print(s["consistency"])
