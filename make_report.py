import json, os, sys
from datetime import datetime, timezone
from pathlib import Path
import requests

source = Path("pytest-report.json")
raw = json.loads(source.read_text(encoding="utf-8")) if source.exists() else {}
tests = []
for item in raw.get("tests", []):
    outcome = item.get("outcome", "unknown")
    call = item.get("call", {})
    error = call.get("crash", {}).get("message") if outcome == "failed" else None
    tests.append({
        "name": item.get("nodeid", "unknown"),
        "result": outcome.upper(),
        "failure_message": error
    })
summary = raw.get("summary", {})
passed = int(summary.get("passed", 0))
failed = int(summary.get("failed", 0)) + int(summary.get("error", 0))
skipped = int(summary.get("skipped", 0))
report = {
    "repository": os.getenv("GITHUB_REPOSITORY", "local-run"),
    "branch": os.getenv("GITHUB_REF_NAME", "local"),
    "commit_sha": os.getenv("GITHUB_SHA", "local"),
    "pipeline_run_id": os.getenv("GITHUB_RUN_ID", "local"),
    "execution_timestamp": datetime.now(timezone.utc).isoformat(),
    "tests": tests,
    "summary": {
        "total": len(tests),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "status": "PASSED" if failed == 0 and tests else "FAILED"
    }
}
Path("test-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
url = os.getenv("REPORT_RECEIVER_URL", "").rstrip("/")
if url:
    try:
        response = requests.post(url + "/report", json=report, timeout=20)
        response.raise_for_status()
        print("Report sent to local receiver:", response.text)
    except Exception as exc:
        print(f"Could not send report to receiver: {exc}", file=sys.stderr)
        sys.exit(2)
else:
    print("REPORT_RECEIVER_URL is not set; report created locally in the CI workspace only.")
