"""
Proves the workbook's formulas reproduce the Python register.

    # LibreOffice (what CI uses): recalculate a copy, then check the saved values
    python src/recalc_libreoffice.py deliverables/ai_act_hr_register.xlsx build/
    python src/check_workbook.py build/ai_act_hr_register.xlsx

    # the pure-Python `formulas` package (quick to run locally)
    python src/check_workbook.py --formulas deliverables/ai_act_hr_register.xlsx

The check fails on any formula error anywhere in the workbook, and on any row of the Reconciliation sheet that does
not match.
"""
import argparse
import sys
from pathlib import Path

import excel_twin as et
from excel_twin import values_from_formulas, values_from_saved
from excel_twin.reconcile import Layout

LAYOUT = Layout()


def check(values: dict, n_checks: int | None = None) -> int:
    report = et.check(values, n_checks, LAYOUT)
    report.print()
    return 0 if report.ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("workbook", type=Path)
    ap.add_argument("--formulas", action="store_true", help="calculate with `formulas` instead of reading saved values")
    args = ap.parse_args()
    values = values_from_formulas(args.workbook) if args.formulas else values_from_saved(args.workbook)
    return check(values)


if __name__ == "__main__":
    sys.exit(main())
