<<<<<<< HEAD
# Assignment Submission Portal

A small Flask portal with required-field and URL validation, pytest automated tests, a GitHub Actions CI pipeline, and a localhost JSON report receiver.

## Requirements
- Python 3.10 or newer
- Git
- GitHub account
- For remote CI report delivery: a tunnel such as ngrok and its authentication token

## Run the portal
```bash
python -m venv .venv
# Windows Command Prompt:
.venv\Scripts\activate
# Windows PowerShell:
# .\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000.

## Run tests locally
```bash
python -m pytest -v --json-report --json-report-file=pytest-report.json
python make_report.py
```

## Start the local report receiver
In a second terminal, activate the environment and run:
```bash
python receiver.py
```
The receiver listens on port 8000 and saves received reports to `test-report.json` in the project directory.

## Connect GitHub Actions to the local receiver
A GitHub-hosted runner cannot access your computer's `localhost` directly. Keep `python receiver.py` running and start a secure tunnel to port 8000, for example with ngrok:
```bash
ngrok http 8000
```
Copy the HTTPS forwarding URL from ngrok. In GitHub, open the repository's **Settings → Secrets and variables → Actions → New repository secret**. Name it `REPORT_RECEIVER_URL` and set its value to the HTTPS forwarding URL (for example `https://your-assigned-domain.ngrok-free.app`, without `/report`). Do not commit tunnel credentials or secrets.

Keep the receiver and tunnel running during each push/demo. The receiver overwrites `test-report.json` with the latest received report. The CI job attempts to send the report after both passing and failing test runs.

## Push to GitHub
Create an empty GitHub repository, then run these commands from this project directory:
```bash
git init
git add .
git commit -m "Create assignment portal and automated tests"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```
Replace the remote URL with your actual repository URL. Future updates:
```bash
git add .
git commit -m "Update assignment portal"
git push
```

## Required tests
1. Complete valid submission is saved and displayed.
2. Missing registration number is rejected with a validation message.
3. Invalid URL is rejected and not saved.

## Demonstration
1. Push the correct version and show all tests passing.
2. Temporarily introduce a defect in URL validation, push it, and show the CI test failure and received JSON report.
3. Restore the correct validation, push again, and show all tests passing.

The local report file is `test-report.json`. It contains repository, branch, commit, run ID, timestamp, individual test results, counts, and overall status when executed in GitHub Actions.
=======
# assignment-submission-portal
>>>>>>> a8a37aea9f36dbe8f3f54df388cb9a1e3ee741cb
