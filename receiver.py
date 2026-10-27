from flask import Flask, request, jsonify
from datetime import datetime, timezone
import json
from pathlib import Path

app = Flask(__name__)
REPORT_PATH = Path(__file__).with_name("test-report.json")

@app.post("/report")
def receive_report():
    report = request.get_json(silent=True)
    if not isinstance(report, dict) or "tests" not in report or "summary" not in report:
        return jsonify({"error": "Invalid report format"}), 400
    report["received_at"] = datetime.now(timezone.utc).isoformat()
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return jsonify({"message": "Report saved", "path": str(REPORT_PATH)}), 200

@app.get("/")
def health():
    return jsonify({"status": "receiver running", "endpoint": "POST /report"})

if __name__ == "__main__":
    # Listen on all interfaces so a tunnel client can forward traffic to this port.
    app.run(host="0.0.0.0", port=8000, debug=False)
