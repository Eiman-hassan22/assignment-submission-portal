import pytest
from app import app, submissions

@pytest.fixture(autouse=True)
def clear_submissions():
    submissions.clear()
    yield
    submissions.clear()

def test_complete_details_and_valid_url_are_saved():
    client = app.test_client()
    response = client.post("/submit", data={
        "name": "Ali Khan",
        "registration_number": "FA24-BSE-016",
        "assignment_title": "DevOps Lab",
        "submission_url": "https://example.com/assignment"
    })
    assert response.status_code == 200
    assert b"Assignment submitted successfully" in response.data
    assert len(submissions) == 1
    assert b"FA24-BSE-016" in response.data

def test_missing_registration_number_is_rejected():
    client = app.test_client()
    response = client.post("/submit", data={
        "name": "Ali Khan",
        "registration_number": "",
        "assignment_title": "DevOps Lab",
        "submission_url": "https://example.com/assignment"
    })
    assert response.status_code == 400
    assert b"Registration Number is required" in response.data
    assert len(submissions) == 0

def test_invalid_submission_url_is_rejected_and_not_saved():
    client = app.test_client()
    response = client.post("/submit", data={
        "name": "Ali Khan",
        "registration_number": "FA24-BSE-016",
        "assignment_title": "DevOps Lab",
        "submission_url": "not-a-valid-url"
    })
    assert response.status_code == 400
    assert b"valid HTTP or HTTPS" in response.data
    assert len(submissions) == 0
