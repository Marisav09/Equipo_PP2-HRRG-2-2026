from __future__ import annotations

from app import create_app


def test_technician_console_requires_login():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/tecnico")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_sets_technician_cookie():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.post("/api/auth/login", json={"password": "tecnico-hrrg"})

    assert response.status_code == 200
    assert "hrrg_technician_auth=ok" in response.headers["Set-Cookie"]


def test_logout_clears_technician_cookie():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    client.post("/api/auth/login", json={"password": "tecnico-hrrg"})
    response = client.post("/api/auth/logout", json={})

    assert response.status_code == 200
    assert "hrrg_technician_auth=;" in response.headers["Set-Cookie"]
