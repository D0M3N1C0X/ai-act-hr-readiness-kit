"""Recalculates a copy of the workbook with LibreOffice, for CI: python src/recalc_libreoffice.py FILE OUTDIR"""
import sys
from pathlib import Path

from excel_twin.recalc import recalc

if __name__ == "__main__":
    print(recalc(Path(sys.argv[1]), Path(sys.argv[2])))
