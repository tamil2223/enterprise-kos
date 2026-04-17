from fastapi.testclient import TestClient


def test_playground_upload_txt_and_md():
    from app.main import app

    with TestClient(app) as client:
        run_id = client.post("/playground/runs").json()["run_id"]

        files = [
            ("files", ("a.txt", b"hello mcp gateway", "text/plain")),
            ("files", ("b.md", b"# Title\n\nhybrid retrieval bm25", "text/markdown")),
        ]
        r = client.post(f"/playground/runs/{run_id}/documents:upload", files=files)
        assert r.status_code == 200
        body = r.json()
        assert body["uploaded"] == 2

        docs = client.get(f"/playground/runs/{run_id}/documents").json()["documents"]
        assert len(docs) == 2


def test_playground_upload_rejects_pdf():
    from app.main import app

    with TestClient(app) as client:
        run_id = client.post("/playground/runs").json()["run_id"]
        files = [("files", ("x.pdf", b"%PDF-1.4", "application/pdf"))]
        r = client.post(f"/playground/runs/{run_id}/documents:upload", files=files)
        assert r.status_code == 400

