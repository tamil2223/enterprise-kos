from app.playground.structured_chunking import chunk_structured_document, parse_sections


def test_parse_markdown_headings_build_paths():
    text = "# A\n\none.\n\n## B\n\ntwo.\n\n### C\n\nthree.\n"
    sections = parse_sections(text=text, doc_id="d1", content_type="text/markdown")
    assert [s.title for s in sections] == ["A", "B", "C"]
    assert sections[0].heading_path == "A"
    assert sections[1].heading_path == "A > B"
    assert sections[2].heading_path == "A > B > C"


def test_structured_chunks_have_metadata_and_embed_header():
    text = "# Title\n\n" + " ".join([f"Sentence {i}." for i in range(1, 25)])
    chunks = chunk_structured_document(
        text=text,
        doc_id="d1",
        source_name="doc.md",
        content_type="text/markdown",
        target_chunk_chars=120,
        max_chunk_chars=220,
        overlap=40,
    )
    assert chunks
    assert all(c.strategy == "structured" for c in chunks)
    assert all(c.section_id for c in chunks)
    assert all(c.heading_path for c in chunks)
    assert all(c.source_name == "doc.md" for c in chunks)
    assert all(c.embed_text and c.embed_text.startswith("doc: doc.md | path:") for c in chunks)
    assert all(c.text in text for c in chunks)


def test_structured_overlap_does_not_cross_plaintext_sections():
    text = (
        "ITEM 1 Business\n"
        "Sentence one. Sentence two. Sentence three.\n"
        "\n"
        "ITEM 2 Risk factors\n"
        "Sentence four. Sentence five. Sentence six.\n"
    )
    chunks = chunk_structured_document(
        text=text,
        doc_id="d2",
        source_name="sec.txt",
        content_type="text/plain",
        target_chunk_chars=40,
        max_chunk_chars=120,
        overlap=30,
    )
    assert len(chunks) >= 2
    # Ensure no chunk simultaneously contains markers from two different ITEM sections.
    for c in chunks:
        has_item1 = "ITEM 1" in c.text
        has_item2 = "ITEM 2" in c.text
        assert not (has_item1 and has_item2)
