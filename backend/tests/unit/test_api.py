import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["app"] == "RankScope API"
    assert data["status"] == "online"


def test_health_endpoint():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_auth_flow_and_project_crud():
    # 1. Register a test user
    email = f"user_test_{pytest.importorskip('uuid').uuid4().hex[:6]}@example.com"
    reg_res = client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "StrongPassword123!", "full_name": "Test User"},
    )
    assert reg_res.status_code == 201
    user_data = reg_res.json()
    assert user_data["email"] == email

    # 2. Login
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "StrongPassword123!"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Get /me
    me_res = client.get("/api/v1/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == email

    # 4. Create Project
    proj_res = client.post(
        "/api/v1/projects",
        json={"name": "SEO Campaign 2026", "description": "Primary domain tracking"},
        headers=headers,
    )
    assert proj_res.status_code == 201
    project_id = proj_res.json()["id"]
    assert proj_res.json()["name"] == "SEO Campaign 2026"

    # 5. List Projects
    list_res = client.get("/api/v1/projects", headers=headers)
    assert list_res.status_code == 200
    assert any(p["id"] == project_id for p in list_res.json())

    # 6. Add Domain to Project
    dom_res = client.post(
        "/api/v1/domains",
        json={
            "domain": "https://example.com/",
            "project_id": project_id,
            "display_name": "Example Corp",
            "is_primary": True,
        },
        headers=headers,
    )
    assert dom_res.status_code == 201
    domain_data = dom_res.json()
    assert domain_data["domain"] == "example.com"  # cleaned
    domain_id = domain_data["id"]

    # 7. List Domains
    dom_list_res = client.get(f"/api/v1/domains?project_id={project_id}", headers=headers)
    assert dom_list_res.status_code == 200
    assert len(dom_list_res.json()) >= 1
