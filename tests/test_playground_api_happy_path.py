from fastapi.testclient import TestClient


def test_playground_happy_path():
    from app.main import app

    with TestClient(app) as client:
        run = client.post("/playground/runs").json()
        run_id = run["run_id"]

        summary = client.get(f"/playground/runs/{run_id}").json()
        assert summary["run_id"] == run_id
        assert summary["documents_count"] == 0
        assert summary["has_index"] is False

        client.post(f"/playground/runs/{run_id}/documents:load-sample").raise_for_status()
        docs = client.get(f"/playground/runs/{run_id}/documents").json()
        doc_id = docs["documents"][0]["doc_id"]

        client.post(
            f"/playground/runs/{run_id}/chunk",
            json={"doc_id": doc_id, "chunk_size": 500, "overlap": 100, "strategy": "window"},
        ).raise_for_status()
        client.post(f"/playground/runs/{run_id}/embed", json={"doc_id": doc_id}).raise_for_status()
        client.post(f"/playground/runs/{run_id}/index").raise_for_status()

        r = client.post(
            f"/playground/runs/{run_id}/retrieve",
            json={"query": "mcp gateway", "top_k": 5},
        )
        assert r.status_code == 200
        body = r.json()
        assert "results" in body
        assert isinstance(body["results"], list)
        assert len(body["results"]) <= 5

