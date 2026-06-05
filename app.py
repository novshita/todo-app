from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []


@app.route("/")
def index():
    edit_id = request.args.get("edit", type=int, default=-1)
    return render_template("index.html", tasks=tasks, edit_id=edit_id)


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    priority = request.form.get("priority", "medium")
    due_date = request.form.get("due_date", "")
    if task:
        tasks.append({"text": task, "done": False, "priority": priority, "due_date": due_date})
    return redirect(url_for("index"))


@app.route("/edit/<int:task_id>", methods=["POST"])
def edit(task_id):
    if 0 <= task_id < len(tasks):
        new_text = request.form.get("text")
        if new_text:
            tasks[task_id]["text"] = new_text
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
