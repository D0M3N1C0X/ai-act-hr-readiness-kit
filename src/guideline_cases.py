"""
The classification put to the test, two ways.

1. **Against the Commission's own examples.** The guidelines on prohibited practices (C(2025) 5052 final, 29 July
   2025, section 7) work through twenty-one workplace cases of emotion recognition with a verdict each:
   data/guideline_cases.csv records each case's facts (whose emotions, from what data, emotion or physical state,
   for what purpose) and the verdict, with its paragraph. Each case is turned into the two answers the register asks
   (infers_emotions, medical_or_safety) the way a reader of the question would give them, then classified by
   register.classify. That is done twice: with the questions as the kit first worded them, read literally, and
   with the questions as reworded from the guidelines. Where the register and the guidelines disagree, the question
   is wrong, not the reader.
2. **Fragility.** For each of the register's systems, every answer is changed one at a time to each of its other
   allowed values and the system classified again: a class that one answer can change is a class to document with
   care, and the answer that changes it is the one to evidence.
"""
import pandas as pd

import register
from config import CHOICES, DATA, PROHIBITED

CASES = DATA / "guideline_cases.csv"
SOURCE = ("Commission Guidelines on prohibited artificial intelligence practices established by Regulation (EU) "
          "2024/1689 (AI Act), C(2025) 5052 final, 29 July 2025, section 7")

# The question as first worded: "Does it read emotions from people's faces, voices or words?" and "Is that only for
# medical or safety reasons? For example, detecting fatigue in drivers." Read literally: anyone's emotions, from any
# data, and any purpose a reader would call health or safety.
OLD_HEALTH = {"medical", "safety", "wellbeing", "property"}
# As reworded: the emotions of workers or candidates, from their face, voice, gestures or typing, not text, not a
# physical state like fatigue, not an expression counted without reading an emotion; answer No when the results
# serve only the worker's own training and never reach HR. Medical or safety: a medical use, or protecting life and
# health against a specific danger; never wellbeing, stress or burnout in general, never property.
NEW_HEALTH = {"medical", "safety"}


def load() -> pd.DataFrame:
    return pd.read_csv(CASES, dtype={"paragraph": int})


def answers(case: dict, wording: str) -> dict:
    """The two answers a reader of the register's questions gives for a case, under the old or the new wording."""
    if wording == "old":
        emotions = case["infers"] == "emotion"
        health = case["purpose"] in OLD_HEALTH
    else:
        emotions = (case["infers"] == "emotion" and case["basis"] == "biometric"
                    and case["target"] in ("workers", "candidates") and case["purpose"] != "training_only")
        health = case["purpose"] in NEW_HEALTH
    return {"infers_emotions": "Yes" if emotions else "No",
            "medical_or_safety": "Yes" if emotions and health else "No"}


# Every other answer set so the case can only be prohibited or not: no Annex III area, no interaction.
NEUTRAL = {"annex_iii": "None", "profiling": "No", "art6_3_condition": "None", "interacts": "No"}


def evaluate() -> pd.DataFrame:
    rows = []
    for c in load().to_dict("records"):
        row = {**c}
        for wording in ("old", "new"):
            a = answers(c, wording)
            cls = register.classify({**NEUTRAL, **a})
            got = "Prohibited" if cls == PROHIBITED else "Not prohibited"
            row[f"{wording}_answer"] = a["infers_emotions"] + (" / medical or safety" if a["medical_or_safety"] == "Yes"
                                                               else "")
            row[f"{wording}_verdict"] = got
            row[f"{wording}_agrees"] = got == c["verdict"]
        rows.append(row)
    return pd.DataFrame(rows)


def alternatives(column: str, value: str) -> list[str]:
    if column in CHOICES:
        return [v for v in CHOICES[column] if v != value]
    if column in register.YES_NO:
        return ["No" if value == "Yes" else "Yes"]
    return []


# The answers that can move a class (the country flags, scope and the questions about duties cannot).
CLASS_ANSWERS = ["infers_emotions", "medical_or_safety", "annex_iii", "profiling", "art6_3_condition", "interacts"]


def fragility(systems: pd.DataFrame | None = None) -> pd.DataFrame:
    systems = register.load() if systems is None else systems
    rows = []
    for s in systems.to_dict("records"):
        cls = register.classify(s)
        flips = []
        for col in CLASS_ANSWERS:
            for alt in alternatives(col, s[col]):
                new = register.classify({**s, col: alt})
                if new != cls:
                    flips.append((col, alt, new))
        rows.append({"system_id": s["system_id"], "system": s["system"], "class": cls, "flips": len(flips),
                     "answers": sorted({f[0] for f in flips}),
                     "to": sorted({f[2] for f in flips})})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pd.set_option("display.width", 220)
    e = evaluate()
    print(e[["case_id", "paragraph", "verdict", "old_verdict", "new_verdict"]].to_string())
    print("old agrees", int(e["old_agrees"].sum()), "new agrees", int(e["new_agrees"].sum()), "of", len(e))
    print(fragility().to_string())
