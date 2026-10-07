import os
import time
from flask import Flask, request, redirect, url_for, render_template_string
import psycopg2
import redis

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "task3db")
DB_USER = os.getenv("POSTGRES_USER", "task3user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "task3pass")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

HTML = """
<!doctype html>
<html>
<head>
    <title>Docker Task 03</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 850px; margin: 40px auto; padding: 0 15px; }
        input { padding: 8px; width: 65%; }
        button { padding: 8px 14px; }
        .box { border: 1px solid #ddd; padding: 15px; margin-bottom: 18px; border-radius: 6px; }
        li { margin: 6px 0; }
    </style>
</head>
<body>
    <h2>RabTech Task 03 - Docker Demo</h2>
    <p>A small Flask application using PostgreSQL and Redis.</p>
    <div class="box">
        <b>PostgreSQL:</b> {{ db_status }}<br>
        <b>Redis:</b> {{ redis_status }}
    </div>
    <div class="box">
        <form method="post" action="{{ url_for('add_note') }}">
            <input name="note" placeholder="Write a small note" required>
            <button type="submit">Add</button>
        </form>
    </div>
    <div class="box">
        <h3>Notes</h3>
        <ul>
        {% for note in notes %}
            <li>{{ note }}</li>
        {% else %}
            <li>No notes yet.</li>
        {% endfor %}
        </ul>
    </div>
</body>
</html>
"""


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=3,
    )


def init_db():
    last_error = None
    for _ in range(30):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY, note TEXT NOT NULL)"
            )
            conn.commit()
            cur.close()
            conn.close()
            return
        except Exception as exc:
            last_error = exc
            time.sleep(2)
    raise RuntimeError(f"Database was not ready: {last_error}")


def get_notes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT note FROM notes ORDER BY id DESC")
    notes = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return notes


@app.get("/")
def index():
    db_status = "Connected"
    redis_status = "Connected"
    try:
        notes = get_notes()
    except Exception:
        db_status = "Not available"
        notes = []
    try:
        redis.Redis(host=REDIS_HOST, port=6379, socket_connect_timeout=1).ping()
    except Exception:
        redis_status = "Not available"
    return render_template_string(HTML, notes=notes, db_status=db_status, redis_status=redis_status)


@app.post("/add")
def add_note():
    note = request.form.get("note", "").strip()
    if note:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO notes (note) VALUES (%s)", (note,))
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for("index"))


@app.get("/health")
def health():
    try:
        conn = get_db_connection()
        conn.close()
        redis.Redis(host=REDIS_HOST, port=6379, socket_connect_timeout=1).ping()
        return {"status": "ok"}, 200
    except Exception as exc:
        return {"status": "not ready", "error": str(exc)}, 503


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
