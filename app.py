import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE = os.environ.get("DATABASE_PATH", "tasks.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DATABASE) or ".", exist_ok=True)
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                text     TEXT    NOT NULL,
                done     INTEGER NOT NULL DEFAULT 0,
                priority TEXT    NOT NULL DEFAULT 'medium',
                due_date TEXT             DEFAULT ''
            )
        """)


init_db()


@app.route("/")
def index():
    edit_id = request.args.get("edit", type=int, default=-1)
    with get_db() as conn:
        tasks = conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()
    return render_template("index.html", tasks=tasks, edit_id=edit_id)


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    priority = request.form.get("priority", "medium")
    due_date = request.form.get("due_date", "")
    if task:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO tasks (text, priority, due_date) VALUES (?, ?, ?)",
                (task, priority, due_date)
            )
    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["POST"])
def edit(task_id):
    new_text = request.form.get("text")
    if new_text:
        with get_db() as conn:
            conn.execute("UPDATE tasks SET text = ? WHERE id = ?", (new_text, task_id))
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    with get_db() as conn:
        conn.execute("UPDATE tasks SET done = NOT done WHERE id = ?", (task_id,))
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    with get_db() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
