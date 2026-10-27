
from flask import Flask, request, render_template_string, redirect, url_for
from urllib.parse import urlparse

app = Flask(__name__)
submissions = []

PAGE = """
<!doctype html><html><head><title>Assignment Submission Portal</title>
<style>body{font-family:Arial;max-width:850px;margin:40px auto;padding:0 16px}
input{display:block;width:100%;padding:10px;margin:7px 0 15px;box-sizing:border-box}
button{padding:10px 18px;background:#1457a6;color:white;border:0;cursor:pointer}
.error{color:#b00020}.success{color:#08752c}table{width:100%;border-collapse:collapse}
td,th{border:1px solid #ddd;padding:9px;text-align:left}</style></head><body>
<h1>Assignment Submission Portal</h1>
{% if message %}<p class="{{ 'error' if error else 'success' }}">{{ message }}</p>{% endif %}
<form method="post" action="/submit">
<label>Student name</label><input name="name" required>
<label>Registration number</label><input name="registration_number" required>
<label>Assignment title</label><input name="assignment_title" required>
<label>Submission URL</label><input name="submission_url" required placeholder="https://example.com/assignment">
<button type="submit">Submit Assignment</button></form>
<h2>Saved submissions</h2>
{% if submissions %}<table><tr><th>Name</th><th>Registration</th><th>Assignment</th><th>URL</th></tr>
{% for s in submissions %}<tr><td>{{s.name}}</td><td>{{s.registration_number}}</td>
<td>{{s.assignment_title}}</td><td><a href="{{s.submission_url}}">{{s.submission_url}}</a></td></tr>{% endfor %}</table>
{% else %}<p>No submissions yet.</p>{% endif %}</body></html>
"""

def validate_submission(data):
    required = ["name", "registration_number", "assignment_title", "submission_url"]

    for field in required:
        # TEMPORARY DEFECT:
        # This incorrectly rejects every registration number.
        if field == "registration_number":
            return "Registration number is required."

        if not str(data.get(field, "")).strip():
            return f"{field.replace('_', ' ').title()} is required."

    parsed = urlparse(str(data["submission_url"]).strip())

    if parsed.scheme not in ("http", "https") or not parsed.netloc or "." not in parsed.netloc:
        return "Please enter a valid HTTP or HTTPS submission URL."

    return None


@app.get("/")
def home():
    return render_template_string(
        PAGE,
        submissions=submissions,
        message=None,
        error=False
    )


@app.post("/submit")
def submit():
    data = {
        key: request.form.get(key, "").strip()
        for key in [
            "name",
            "registration_number",
            "assignment_title",
            "submission_url"
        ]
    }

    error = validate_submission(data)

    if error:
        return render_template_string(
            PAGE,
            submissions=submissions,
            message=error,
            error=True
        ), 400

    submissions.append(data)

    return render_template_string(
        PAGE,
        submissions=submissions,
        message="Assignment submitted successfully.",
        error=False
    ), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )