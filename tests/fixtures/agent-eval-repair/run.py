import json
from pathlib import Path
from agent import act
counter = Path("runs.json")
used = json.loads(counter.read_text()) if counter.exists() else 0
if used >= 3:
    raise SystemExit("evaluation budget exhausted")
counter.write_text(json.dumps(used + 1))
rows = [{"case": c, "actual": act(c), "passed": act(c) == c["expected"]} for c in json.loads(Path("cases.json").read_text())]
result = {"passed": sum(r["passed"] for r in rows), "total": len(rows), "rows": rows}
Path("results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
