
import os
import json
import smtplib
from email.message import EmailMessage


# Get Gmail credentials from GitHub Secrets
email_address = os.environ["EMAIL_ADDRESS"]
app_password = os.environ["EMAIL_APP_PASSWORD"]


# Read the test report
with open("test-report.json", "r", encoding="utf-8") as f:
    report = json.load(f)


# Get report information
status = report["summary"]["status"]
passed = report["summary"]["passed"]
failed = report["summary"]["failed"]
total = report["summary"]["total"]


# Create email
msg = EmailMessage()

msg["Subject"] = f"Assignment Portal Test Report - {status}"
msg["From"] = email_address
msg["To"] = email_address

msg.set_content(f"""
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
""")


# Connect to Gmail SMTP
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_address, app_password)
        server.send_message(msg)

    print("Email sent successfully!")

except Exception as e:
    print("Email sending failed:")
    print(str(e))
    raise
