from fastapi.testclient import TestClient


def test_health_ok():
    from app.main import app

    with TestClient(app) as client:
        resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_context_returns_context_items():
    from app.main import app

    with TestClient(app) as client:
        resp = client.get("/context", params={"q": "postgres vector", "top_k": 3})
    assert resp.status_code == 200
    body = resp.json()
    assert "contexts" in body
    assert isinstance(body["contexts"], list)
    assert len(body["contexts"]) <= 3


def test_query_returns_answer_and_contexts():
    from app.main import app

    with TestClient(app) as client:
        resp = client.post(
            "/query",
            json={"query": "How does hybrid retrieval work?", "top_k": 2},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert "answer" in body
    assert isinstance(body["answer"], str)
    assert body["answer"].strip()
    assert "contexts" in body
    assert isinstance(body["contexts"], list)


def test_agent_run_returns_steps_and_final():
    from app.main import app

    with TestClient(app) as client:
        resp = client.post("/agent/run", json={"query": "Explain MCP gateway responsibilities"})
    assert resp.status_code == 200
    body = resp.json()
    assert "final" in body
    assert isinstance(body["final"], str)
    assert body["final"].strip()
    assert "steps" in body
    assert isinstance(body["steps"], list)
    assert len(body["steps"]) >= 3
    assert "contexts" in body
