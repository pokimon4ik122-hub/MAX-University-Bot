
import os
from flask import Flask, request, jsonify, render_template_string
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Simple in-memory demo data
STUDENTS = {
    "12345": {"name": "Ivan Petrov", "schedule": ["Mon 9:00 Math", "Tue 11:00 Physics"], "grades": {"Math": "A", "Physics": "B+"}},
    "67890": {"name": "Anna Ivanova", "schedule": ["Mon 10:00 Literature", "Wed 14:00 Chemistry"], "grades": {"Literature": "A-", "Chemistry": "B"}},
}

# Expect MAX_TOKEN in environment for validating incoming requests (simulated)
MAX_TOKEN = os.environ.get("MAX_TOKEN", "demo-token")

# Simple landing page for the mini-app
MINI_APP_HTML = """
<!doctype html>
<title>MAX University Bot - Mini App</title>
<h2>MAX University — Mini App</h2>
<p>This mini-app simulates document requests and support tickets.</p>

<form action="/mini/request_document" method="post">
  Student ID: <input name="student_id"><br>
  Document type:
  <select name="doc_type">
    <option>Enrollment Certificate</option>
    <option>Transcript</option>
    <option>Diploma Supplement</option>
  </select><br>
  <button type="submit">Request Document</button>
</form>

<form action="/mini/support" method="post" style="margin-top:20px;">
  Student ID: <input name="student_id"><br>
  Issue: <input name="issue_description" style="width:400px;"><br>
  <button type="submit">Open Support Ticket</button>
</form>
"""

@app.route("/")
def index():
    return "MAX University Bot - alive. Use /webhook for webhook POSTs or /mini for mini-app."

@app.route("/mini", methods=["GET"])
def mini_home():
    return MINI_APP_HTML

@app.route("/mini/request_document", methods=["POST"])
def mini_request_document():
    student_id = request.form.get("student_id")
    doc_type = request.form.get("doc_type")
    if not student_id:
        return "Provide student_id", 400
    # In real app would create ticket and send to SIS
    return f"Document request received for {student_id}: {doc_type}. We'll email you when ready."

@app.route("/mini/support", methods=["POST"])
def mini_support():
    student_id = request.form.get("student_id")
    issue = request.form.get("issue_description")
    if not student_id or not issue:
        return "Provide student_id and issue_description", 400
    return f"Support ticket opened for {student_id}. Issue: {issue}"

# Webhook endpoint to receive messages from MAX messenger (simulated)
@app.route("/webhook", methods=["POST"])
def webhook():
    # Validate token header (this simulates MAX's signature/auth)
    token = request.headers.get("X-MAX-TOKEN", "")
    if token != MAX_TOKEN:
        return jsonify({"error": "invalid token"}), 403

    data = request.get_json() or {}
    logging.info("Received webhook data: %s", data)

    # Very simple message handling logic
    user_id = data.get("user_id")
    text = (data.get("text") or "").strip().lower()

    # responses
    if text.startswith("start") or text == "/start":
        return jsonify({"reply": f"Привет! Я бот вуза. Введите ваш студенческий ID, например: id 12345"})
    if text.startswith("id "):
        sid = text.split(" ",1)[1].strip()
        student = STUDENTS.get(sid)
        if not student:
            return jsonify({"reply": "Студенческий ID не найден. Проверьте и попробуйте снова."})
        return jsonify({"reply": f"Добро пожаловать, {student['name']}! Доступные команды: schedule, grades, request doc <type>, support <issue>"})
    if text == "schedule":
        # For demo assume user has id in payload
        sid = data.get("student_id")
        student = STUDENTS.get(sid)
        if not student:
            return jsonify({"reply": "Не указан студент. Используйте 'id <ваш_id>' сначала."})
        return jsonify({"reply": "Ваш расписание:\n" + "\\n".join(student["schedule"])})
    if text == "grades":
        sid = data.get("student_id")
        student = STUDENTS.get(sid)
        if not student:
            return jsonify({"reply": "Не указан студент. Используйте 'id <ваш_id>' сначала."})
        grades = "\\n".join([f"{k}: {v}" for k,v in student["grades"].items()])
        return jsonify({"reply": "Ваши оценки:\\n" + grades})
    if text.startswith("request doc"):
        sid = data.get("student_id")
        if not sid:
            return jsonify({"reply": "Не указан студент. Используйте 'id <ваш_id>'."})
        doc = text.replace("request doc","").strip()
        if not doc:
            doc = "Enrollment Certificate"
        return jsonify({"reply": f"Запрос на документ '{doc}' принят. Номер заявки: RQ-1001"})
    if text.startswith("support"):
        sid = data.get("student_id")
        issue = text.replace("support","").strip()
        if not issue:
            return jsonify({"reply": "Опишите проблему после команды support"})
        return jsonify({"reply": f"Тикет создан: {issue}. Номер: TKT-2001"})

    return jsonify({"reply": "Не понимаю команду. Попробуйте: id <ваш_id>, schedule, grades, request doc <type>, support <issue>."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
