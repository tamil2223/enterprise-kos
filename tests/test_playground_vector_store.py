from app.playground.vector_store import VectorStore


def test_vector_store_topk():
    vs = VectorStore(dim=3)
    vs.add("v1", [1.0, 0.0, 0.0], meta={"chunk_id": "c1"})
    vs.add("v2", [0.0, 1.0, 0.0], meta={"chunk_id": "c2"})
    results = vs.search([1.0, 0.0, 0.0], top_k=1)
    assert results[0].vector_id == "v1"
    assert results[0].meta["chunk_id"] == "c1"

