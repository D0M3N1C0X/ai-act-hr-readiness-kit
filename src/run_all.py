"""Rebuilds every output from data/: the register workbook, the report and its page. Takes a few seconds."""
import time

import build_report
import build_web
import build_workbook

if __name__ == "__main__":
    t0 = time.time()
    m = build_workbook.build()
    print(f"workbook -> deliverables/ai_act_hr_register.xlsx ({len(m.checks)} reconciliation checks)")
    build_report.main()
    build_web.main()
    print(f"done in {time.time() - t0:.1f}s")
