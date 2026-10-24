"""The figures quoted in the README are the ones the pipeline produces."""
from pathlib import Path

import build_workbook
import register
from config import ASSESSMENT_DATE, D_ANNEX_III

README = (Path(__file__).resolve().parent.parent / "README.md").read_text(encoding="utf-8")
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]


def test_readme_quotes_current_figures(tmp_path):
    s = register.summary(register.build())
    expected = [
        f"{WORDS[s['n_High-risk']].capitalize()} of {WORDS[s['systems']]} systems are high-risk",
        f"{(D_ANNEX_III - ASSESSMENT_DATE).days} days from this assessment",
        f"staff using {s['obligations']['O01']} systems",
        f"talking to an AI is the supplier's duty for {s['obligations']['O03']}",
        f"{s['worker_rules']['W-DE1']} systems to inform it about, "
        f"at least {s['worker_rules']['W-DE2']} that need its agreement",
        f"parameters of {s['worker_rules']['W-ES1']} systems",
        f"a written notice for {s['worker_rules']['W-IT1']} fully automated system",
        f"reconciled on {len(build_workbook.build(tmp_path / 'm.xlsx').checks)} checks",
        f"({s['workers_total']:,} workers)",
    ]
    missing = [e for e in expected if e not in README]
    assert not missing, f"README is out of date: {missing}"
