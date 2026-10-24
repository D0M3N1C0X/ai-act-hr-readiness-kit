"""The browser tool's inputs and test cases match what the pipeline writes now."""
import json

import build_web
from config import ROOT


def test_inputs_and_vectors_are_current(tmp_path, monkeypatch):
    committed = json.loads((ROOT / "web" / "inputs.json").read_text(encoding="utf-8"))
    assert committed == build_web.cfg()
    vectors = json.loads((ROOT / "tests" / "fixtures" / "js_vectors.json").read_text(encoding="utf-8"))
    assert vectors["cfg"] == build_web.cfg()
    assert len(vectors["cases"]) >= 2000 + 12
