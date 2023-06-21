from flask import session
from conftests import app, client


def test_index_redirect(client):
    response = client.get("/")
    assert response.status_code == 302
    assert response.location == "/login"


def test_login_get(client):
    response = client.get("/login")
    assert response.status_code == 200


def test_chat_get_without_session(client):
    response = client.get("/chat")
    assert response.status_code == 302
    assert response.location.startswith("/login")


def test_home_get_without_session(client):
    response = client.get("/home")
    response = client.get("/chat")
    assert response.status_code == 302
    assert response.location.startswith("/login")
