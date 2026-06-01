import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module
from app import app, todos


@pytest.fixture(autouse=True)
def reset():
    todos.clear()
    app_module.next_id = 1
    yield


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_creer_todo(client):
    client.post("/todos", data={"title": "Acheter du pain"}, follow_redirects=True)
    assert len(todos) == 1
    assert todos[0]["title"] == "Acheter du pain"
    assert todos[0]["done"] is False


def test_creer_todo_titre_vide(client):
    client.post("/todos", data={"title": ""}, follow_redirects=True)
    assert len(todos) == 0


def test_supprimer_todo(client):
    client.post("/todos", data={"title": "A supprimer"}, follow_redirects=True)
    client.post("/todos/1/delete", follow_redirects=True)
    assert len(todos) == 0


def test_completer_todo(client):
    client.post("/todos", data={"title": "Test"}, follow_redirects=True)
    client.post("/todos/1/complete", follow_redirects=True)
    assert todos[0]["done"] is True


def test_boom_retourne_500(client):
    resp = client.get("/boom")
    assert resp.status_code == 500
