"""
Office files are zip archives stamped with the time they were written; excel-twin rewrites them with fixed
timestamps, and CI compares the decompressed content with the committed file.

    python src/deterministic.py --check deliverables/ai_act_hr_register.xlsx
"""
import sys

from excel_twin.determinism import check_against_git

if __name__ == "__main__":
    if sys.argv[1:2] != ["--check"] or len(sys.argv) < 3:
        raise SystemExit("usage: deterministic.py --check FILE [FILE ...]")
    raise SystemExit(check_against_git(sys.argv[2:]))
