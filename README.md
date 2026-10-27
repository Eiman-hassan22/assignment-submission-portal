# Assignment Submission Portal

## Project Description

This project is an Assignment Submission Portal developed for the DevOps lab midterm. It allows students to submit their assignment details through a web application. The student provides their name, registration number, assignment title, and submission URL.

The application validates the required fields and checks that the submission URL is a valid HTTP or HTTPS URL. Valid submissions are saved and displayed on the portal.

## Project Technologies

- Python
- Flask
- Pytest
- GitHub Actions
- GitHub
- Self-hosted GitHub Actions Runner

## Project Structure

```text
assignment-submission-portal/
│
├── app.py
├── receiver.py
├── make_report.py
├── requirements.txt
├── pytest.ini
├── test-report.json
├── README.md
│
├── tests/
│   └── test_app.py
│
└── .github/
    └── workflows/
        └── ci.yml
```

## How to Run the Application

First install the required packages:

```bash
python -m pip install -r requirements.txt
```

Then start the Flask application:

```bash
python app.py
```

The application runs locally on:

```text
http://127.0.0.1:5000
```

Open this address in a web browser to use the Assignment Submission Portal.

## How to Run Automated Tests

The project contains three automated tests.

Run all tests using:

```bash
python -m pytest -v
```

The tests check:

1. Complete assignment details with a valid URL are accepted and saved.
2. A missing registration number is rejected.
3. An invalid submission URL is rejected and not saved.

## Continuous Integration

GitHub Actions is used for continuous integration.

Whenever code is pushed to the `main` branch, the workflow automatically:

1. Checks out the project.
2. Installs the required dependencies.
3. Runs the automated tests.
4. Generates the test report.
5. Sends the report to the local HTTP receiver.
6. Fails the pipeline if any automated test fails.

The project uses a self-hosted GitHub Actions runner because the local report receiver needs to be accessible during the pipeline.

## Local Report Receiver

The local HTTP receiver is implemented in `receiver.py`.

Start the receiver using:

```bash
python receiver.py
```

The receiver listens on:

```text
http://127.0.0.1:8000
```

The test report is sent automatically to the receiver after the tests execute.

The receiver saves the report as:

```text
test-report.json
```

## Test Report

The generated `test-report.json` contains:

- Repository name
- Branch name
- Commit SHA
- Pipeline run ID
- Execution timestamp
- Individual test names
- Test results
- Failure messages
- Total tests
- Passed tests
- Failed tests
- Overall status

Both successful and failed pipeline runs are automatically reported.

## CI Failure Demonstration

A defect was intentionally introduced into the application to demonstrate CI failure handling.

The automated tests detected the defect, the GitHub Actions pipeline failed, and the local `test-report.json` was automatically updated with the failed test results.

After fixing the defect, the tests passed again and the GitHub Actions pipeline returned to a successful state.

## Conclusion

The project demonstrates an automated DevOps workflow where application testing is integrated with GitHub Actions. Every push can be automatically tested, and the results are automatically sent to a local report receiver and stored as a JSON report.