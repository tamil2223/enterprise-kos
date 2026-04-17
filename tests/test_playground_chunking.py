import math

from app.playground.chunking import chunk_text_window
from app.playground.embeddings import fake_embed_384


def test_chunking_overlap_boundaries():
    text = "abcdefghijklmnopqrstuvwxyz" * 10
    chunks = chunk_text_window(text=text, chunk_size=50, overlap=10, doc_id="d1")
    assert len(chunks) > 1
    assert chunks[0].start_char == 0
    assert chunks[0].end_char == 50
    assert chunks[1].start_char == 40  # 50 - 10


def test_chunking_ids_and_indices_and_slices_match_text():
    doc_id = "doc-1"
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunk_text_window(text=text, chunk_size=10, overlap=3, doc_id=doc_id)

    assert [c.chunk_id for c in chunks] == [
        "doc-1#chunk-0",
        "doc-1#chunk-1",
        "doc-1#chunk-2",
        "doc-1#chunk-3",
    ]
    assert [c.chunk_index for c in chunks] == [0, 1, 2, 3]
    assert all(c.doc_id == doc_id for c in chunks)

    # Slice bounds are [start, end)
    for c in chunks:
        assert c.text == text[c.start_char : c.end_char]

    assert [(c.start_char, c.end_char) for c in chunks] == [
        (0, 10),
        (7, 17),
        (14, 24),
        (21, 26),
    ]


def test_chunking_overlap_content_matches():
    doc_id = "doc-2"
    text = "0123456789" * 5
    overlap = 4
    chunks = chunk_text_window(text=text, chunk_size=12, overlap=overlap, doc_id=doc_id)
    assert len(chunks) > 2

    for prev, cur in zip(chunks, chunks[1:]):
        assert cur.start_char == prev.end_char - overlap
        assert prev.text[-overlap:] == cur.text[:overlap]


def test_chunking_overlap_zero_steps_forward_by_chunk_size():
    doc_id = "doc-3"
    text = "abcdefghijklmnopqrstuvwxyz"
    chunks = chunk_text_window(text=text, chunk_size=10, overlap=0, doc_id=doc_id)
    assert [(c.start_char, c.end_char) for c in chunks] == [
        (0, 10),
        (10, 20),
        (20, 26),
    ]


def test_chunking_empty_text_returns_empty_list():
    chunks = chunk_text_window(text="", chunk_size=10, overlap=0, doc_id="d")
    assert chunks == []


def test_chunking_text_shorter_than_chunk_size_returns_one_chunk():
    doc_id = "doc-4"
    text = "hello"
    chunks = chunk_text_window(text=text, chunk_size=10, overlap=0, doc_id=doc_id)
    assert len(chunks) == 1
    assert chunks[0].chunk_id == "doc-4#chunk-0"
    assert (chunks[0].start_char, chunks[0].end_char) == (0, 5)
    assert chunks[0].text == "hello"


def test_chunking_validates_parameters():
    try:
        chunk_text_window(text="x", chunk_size=0, overlap=0, doc_id="d")
        assert False, "expected ValueError for chunk_size<=0"
    except ValueError:
        pass

    try:
        chunk_text_window(text="x", chunk_size=10, overlap=-1, doc_id="d")
        assert False, "expected ValueError for overlap<0"
    except ValueError:
        pass

    try:
        chunk_text_window(text="x" * 20, chunk_size=10, overlap=10, doc_id="d")
        assert False, "expected ValueError for overlap>=chunk_size"
    except ValueError:
        pass


def test_fake_embed_dim_and_determinism():
    v1 = fake_embed_384("hello world")
    v2 = fake_embed_384("hello world")
    v3 = fake_embed_384("hello worlds")  # token change => different embedding

    assert isinstance(v1, list)
    assert len(v1) == 384
    assert all(isinstance(x, float) for x in v1)
    assert v1 == v2
    assert v1 != v3

    # L2-normalized (for non-empty inputs)
    norm = math.sqrt(sum(x * x for x in v1))
    assert math.isclose(norm, 1.0, rel_tol=1e-9, abs_tol=1e-12)
