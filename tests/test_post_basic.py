from datetime import datetime, timedelta, timezone
import token
from xml.dom.domreg import registered
from xmlrpc import client
import jwt
import pytest
from routers.auth import login
from security import ALGORITHM, SECRET_KEY, hash_password, verify_password

USER = { "email": "student@example.com", "password": "secret123"}
POST= {
  "title": "Cloud computing discussion",
  "body": "What are the advantages of containers?",
  "topics": [
    "Tech","sport"
  ],
  "expires_at": "2026-12-19T19:14:52.338Z"
}


def test_post_requires_token(client):
    response = client.post("/posts", json=POST)
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_login_and_validpost(client):
    registered = client.post("/auth/register", json=USER)
    assert registered.status_code == 201
    assert set(registered.json()) == {"id", "email"}
    login = client.post("/auth/login", json=USER)
    token = login.json()["access_token"]
    posts = client.post("/posts", headers={"Authorization": f"Bearer {token}"}, json=POST)
    assert posts.status_code == 201



@pytest.mark.parametrize("body", [POST, {**POST, "topics": ["Science"]}, {**POST, "expires_at": "2025-12-19T19:14:52.338Z"}])
def test_bad_post(client, body):
    client.post("/auth/register", json=USER)
    login=client.post("/auth/login", json=USER)
    token = login.json()["access_token"]

    if body["topics"] ==  ["Science"]:
        assert client.post("/posts", headers={"Authorization": f"Bearer {token}"}, json=body).status_code == 422

    elif body["expires_at"] == "2025-12-19T19:14:52.338Z":
        assert client.post("/posts", headers={"Authorization": f"Bearer {token}"}, json=body).status_code == 422    



