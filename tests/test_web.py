"""Tests for the web module."""

from fastapi.testclient import TestClient

from web.app import app

client = TestClient(app)


def test_health_endpoint():
    """GET /health returns ok status."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "haunted-repo"


def test_graveyard_home():
    """GET / returns the graveyard HTML page."""
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Haunted Repo" in response.text
    assert "Graveyard" in response.text


def test_analyze_endpoint_stub():
    """GET /api/analyze returns stub data."""
    response = client.get("/api/analyze?repo_url=https://github.com/example/test")

    assert response.status_code == 200
    data = response.json()
    assert data["repo_url"] == "https://github.com/example/test"
    assert data["status"] == "stub"
    assert "analyzer" in data
    assert "flakes" in data
    assert "deps" in data
