from __future__ import annotations

from app import create_app


def test_technician_console_requires_login():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/tecnico")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_technician_selector_exposes_general_tools_only_to_technicians():
    app = create_app()
    app.config["TESTING"] = True

    technician = app.test_client()
    technician.set_cookie("hrrg_technician_auth", "ok")
    technician_response = technician.get("/tecnico")

    assert technician_response.status_code == 200
    assert b'id="monitoring-button"' in technician_response.data
    assert b'id="manuals-button"' in technician_response.data
    assert b'id="monitoring-dialog"' in technician_response.data

    operator = app.test_client()
    operator.set_cookie("hrrg_operator_auth", "ok")
    operator_response = operator.get("/operador")

    assert operator_response.status_code == 200
    assert b'id="monitoring-button"' not in operator_response.data
    assert b'id="manuals-button"' not in operator_response.data


def test_direct_equipment_url_without_login_returns_home_with_pending_qr_equipment():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/equipo/sterrad-100")

    assert response.status_code == 302
    assert response.headers["Location"] == "/"
    assert "hrrg_qr_equipment_id=sterrad-100" in response.headers["Set-Cookie"]


def test_login_sets_technician_cookie():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.post(
        "/api/auth/login",
        json={"username": "tecnico", "password": "tecnico-hrrg"},
    )

    assert response.status_code == 200
    assert "hrrg_technician_auth=ok" in response.headers["Set-Cookie"]


def test_qr_access_stores_equipment_and_login_redirects_operator_to_chat():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    qr_response = client.get("/qr/sterrad-100")

    assert qr_response.status_code == 302
    assert qr_response.headers["Location"] == "/"
    assert "hrrg_qr_equipment_id=sterrad-100" in qr_response.headers["Set-Cookie"]

    login_response = client.post(
        "/api/auth/login",
        json={"username": "operador", "password": "operador-hrrg", "profile": "operador"},
    )

    assert login_response.status_code == 200
    assert login_response.json["redirect_url"] == "/equipo/sterrad-100"
    assert any(
        "hrrg_qr_equipment_id=;" in cookie
        for cookie in login_response.headers.getlist("Set-Cookie")
    )


def test_qr_access_stores_equipment_and_login_redirects_technician_to_chat():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    qr_response = client.get("/qr/sterrad-100")

    assert qr_response.status_code == 302
    assert qr_response.headers["Location"] == "/"

    login_response = client.post(
        "/api/auth/login",
        json={"username": "tecnico", "password": "tecnico-hrrg", "profile": "tecnico"},
    )

    assert login_response.status_code == 200
    assert login_response.json["redirect_url"] == "/tecnico/equipo/sterrad-100"


def test_qr_access_rejects_unknown_equipment():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    response = client.get("/qr/equipo-inexistente")

    assert response.status_code == 404


def test_logout_clears_technician_cookie():
    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()
    client.post(
        "/api/auth/login",
        json={"username": "tecnico", "password": "tecnico-hrrg"},
    )
    response = client.post("/api/auth/logout", json={})

    assert response.status_code == 200
    assert "hrrg_technician_auth=;" in response.headers["Set-Cookie"]
