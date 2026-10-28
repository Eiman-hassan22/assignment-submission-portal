
import os
import json
import urllib.request
import urllib.error
# Get secrets from GitHub Actions
api_key = os.environ["RESEND_API_KEY"]
to_email = os.environ["EMAIL_TO"]
# Read the generated test report
with open("test-report.json", "r", encoding="utf-8") as f:
    report = json.load(f)
# Get report summary
status = report["summary"]["status"]
passed = report["summary"]["passed"]
failed = report["summary"]["failed"]
total = report["summary"]["total"]
# Email subject
subject = f"Assignment Portal Test Report - {status}"
# Email body
body = f"""
Assignment Submission Portal - Automated Test Report

Repository: {report["repository"]}
Branch: {report["branch"]}
Commit: {report["commit_sha"]}
Pipeline Run: {report["pipeline_run_id"]}
Status: {status}

Test Summary:
Total Tests: {total}
Passed: {passed}
Failed: {failed}

Detailed Results:
{json.dumps(report["tests"], indent=2)}
"""


# Prepare email data
data = json.dumps({
    "from": "Assignment Portal <onboarding@resend.dev>",
    "to": [to_email],
    "subject": subject,
    "text": body
}).encode("utf-8")


# Create Resend API request
request = urllib.request.Request(
    "https://api.resend.com/emails",
    data=data,
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    method="POST"
)


# Send email
try:
    with urllib.request.urlopen(request) as response:
        print("Email sent successfully.")
        print(response.read().decode())

except urllib.error.HTTPError as e:
    print("====================================")
    print("RESEND EMAIL ERROR")
    print("====================================")
    print("HTTP Status:", e.code)
    print("Error Details:")
    print(e.read().decode())
    print("====================================")
    raise

except Exception as e:
    print("Email sending failed:")
    print(str(e))
    raise