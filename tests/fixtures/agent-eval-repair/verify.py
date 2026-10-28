import json
from pathlib import Path
from agent import act
cases = json.loads(Path("cases.json").read_text())
assert all(act(c) == c["expected"] for c in cases)
assert 1 <= json.loads(Path("runs.json").read_text()) <= 3
report = json.loads(Path("results.json").read_text())
assert report["passed"] == report["total"] == 4
assert all(r["passed"] and r["actual"] == act(r["case"]) for r in report["rows"])
print("offline acceptance passed")
