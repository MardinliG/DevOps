import json
import logging
import os
import sys
from datetime import datetime, timezone

from flask import Flask, redirect, render_template_string, request, jsonify, url_for

SERVICE = os.getenv("SERVICE_NAME", "api")
app = Flask(__name__)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

todos = []
next_id = 1


def log(level, msg, **fields):
    entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "service": SERVICE,
        "msg": msg,
    }
    entry.update(fields)
    sys.stdout.write(json.dumps(entry) + "\n")
    sys.stdout.flush()


HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Todo List — Projets 0777</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; padding: 2rem; }
    .container { max-width: 600px; margin: 0 auto; }
    h1 { font-size: 2rem; font-weight: 700; color: #f97316; margin-bottom: 0.25rem; }
    .subtitle { color: #94a3b8; font-size: 0.85rem; margin-bottom: 2rem; }
    .add-form { display: flex; gap: 0.5rem; margin-bottom: 2rem; }
    .add-form input { flex: 1; padding: 0.75rem 1rem; border-radius: 8px; border: 1px solid #334155; background: #1e293b; color: #e2e8f0; font-size: 1rem; }
    .add-form input:focus { outline: none; border-color: #f97316; }
    .btn { padding: 0.75rem 1.5rem; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; transition: opacity 0.15s; }
    .btn:hover { opacity: 0.85; }
    .btn-add    { background: #f97316; color: white; }
    .btn-done   { background: #10b981; color: white; font-size: 0.8rem; padding: 0.4rem 0.75rem; }
    .btn-reopen { background: #64748b; color: white; font-size: 0.8rem; padding: 0.4rem 0.75rem; }
    .btn-delete { background: #ef4444; color: white; font-size: 0.8rem; padding: 0.4rem 0.75rem; }
    .todo-list  { display: flex; flex-direction: column; gap: 0.75rem; }
    .todo-item  { background: #1e293b; border-radius: 10px; padding: 1rem 1.25rem; display: flex; align-items: center; gap: 1rem; border-left: 4px solid #334155; }
    .todo-item.done { border-left-color: #10b981; opacity: 0.65; }
    .todo-title { flex: 1; }
    .todo-title.done { text-decoration: line-through; color: #64748b; }
    .badge { font-size: 0.7rem; background: #334155; color: #94a3b8; padding: 0.15rem 0.4rem; border-radius: 4px; margin-left: 0.4rem; }
    .actions { display: flex; gap: 0.5rem; }
    .empty { text-align: center; color: #475569; padding: 3rem; }
    .boom { margin-top: 2.5rem; text-align: center; }
    .boom a { color: #ef4444; font-size: 0.8rem; opacity: 0.4; text-decoration: none; }
    .boom a:hover { opacity: 1; }
  </style>
</head>
<body>
<div class="container">
  <h1>📋 Todo List</h1>
  <p class="subtitle">Chaque action génère un log JSON → Promtail → Loki → Grafana</p>

  <form class="add-form" method="POST" action="/todos">
    <input name="title" placeholder="Nouvelle tâche..." autofocus required>
    <button class="btn btn-add">Ajouter</button>
  </form>

  <div class="todo-list">
    {% if not todos %}
      <div class="empty">Aucune tâche — ajoutes-en une !</div>
    {% endif %}
    {% for t in todos %}
    <div class="todo-item {{ 'done' if t.done }}">
      <span class="todo-title {{ 'done' if t.done }}">
        {{ t.title }}<span class="badge">#{{ t.id }}</span>
      </span>
      <div class="actions">
        <form method="POST" action="/todos/{{ t.id }}/complete">
          <button class="btn {{ 'btn-reopen' if t.done else 'btn-done' }}">
            {{ 'Rouvrir' if t.done else '✓ Fait' }}
          </button>
        </form>
        <form method="POST" action="/todos/{{ t.id }}/delete">
          <button class="btn btn-delete">✕</button>
        </form>
      </div>
    </div>
    {% endfor %}
  </div>

  <div class="boom"><a href="/boom">⚡ Simuler une erreur 500</a></div>
</div>
</body>
</html>
"""


@app.get("/")
def index():
    done = sum(1 for t in todos if t["done"])
    log("info", "todo list viewed", total=len(todos), done=done, pending=len(todos) - done)
    return render_template_string(HTML, todos=todos)


@app.post("/todos")
def create():
    global next_id
    title = request.form.get("title", "").strip()
    if not title:
        log("error", "todo creation failed", reason="empty title", status=400)
        return redirect(url_for("index"))
    todo = {"id": next_id, "title": title, "done": False}
    todos.append(todo)
    log("info", "todo created", todo_id=next_id, title=title)
    next_id += 1
    return redirect(url_for("index"))


@app.post("/todos/<int:tid>/complete")
def complete(tid):
    todo = next((t for t in todos if t["id"] == tid), None)
    if not todo:
        log("error", "todo not found", todo_id=tid, status=404)
        return redirect(url_for("index"))
    todo["done"] = not todo["done"]
    action = "completed" if todo["done"] else "reopened"
    log("info", f"todo {action}", todo_id=tid, title=todo["title"])
    return redirect(url_for("index"))


@app.post("/todos/<int:tid>/delete")
def delete(tid):
    global todos
    todo = next((t for t in todos if t["id"] == tid), None)
    if not todo:
        log("error", "todo not found", todo_id=tid, status=404)
        return redirect(url_for("index"))
    todos = [t for t in todos if t["id"] != tid]
    log("warn", "todo deleted", todo_id=tid, title=todo["title"])
    return redirect(url_for("index"))


@app.get("/boom")
def boom():
    log("error", "unhandled exception", path="/boom", status=500,
        error="RuntimeError: simulated crash")
    return jsonify(error="internal server error"), 500


if __name__ == "__main__":
    log("info", "todo api starting", port=8080)
    app.run(host="0.0.0.0", port=8080)
