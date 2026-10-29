```python
import os
import json
import smtplib
from email.message import EmailMessage


# Get Gmail credentials from GitHub Secrets
email_address = os.environ["EMAIL_ADDRESS"]
app_password = os.environ["EMAIL_APP_PASSWORD"]


# Read test report
with open("test-report.json", "r", encoding="utf-8") as f:
    report = json.load(f)


# Get report information
status = report["summary"]["status"]
total = report["summary"]["total"]
passed = report["summary"]["passed"]
failed = report["summary"]["failed"]

commit = report["commit_sha"]
short_commit = commit[:7]


# Create individual test result lines
test_lines = ""

for test in report["tests"]:
    # Remove tests/test_app.py:: from test name
    test_name = test["name"].split("::")[-1]

    result = test["result"].lower()

    test_lines += f"- {test_name}: {result}\n"


# Create email
msg = EmailMessage()

msg["Subject"] = f"[Assignment Portal CI] {status} - {short_commit}"
msg["From"] = email_address
msg["To"] = email_address


# Email body
msg.set_content(f"""
CI Test Report

Repository : {report["repository"]}
Branch     : {report["branch"]}
Commit     : {report["commit_sha"]}
Run ID     : {report["pipeline_run_id"]}
Timestamp  : {report["execution_timestamp"]}

Overall Status : {status}
Total          : {total}
Passed         : {passed}
Failed         : {failed}

Individual Tests:
{test_lines}
""")


# Attach test-report.json
with open("test-report.json", "rb") as f:
    report_file = f.read()

msg.add_attachment(
    report_file,
    maintype="application",
    subtype="json",
    filename="test-report.json"
)


# Send email using Gmail SMTP
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_address, app_password)
        server.send_message(msg)

    print("Email sent successfully!")
    print("test-report.json attached successfully!")

except Exception as e:
    print("Email sending failed:")
    print(str(e))
    raise