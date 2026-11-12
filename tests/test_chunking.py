from genomic_parser.chunk_processor import chunk_sequence


def test_chunk_sequence_without_overlap():
    chunks = chunk_sequence("AACCGGTT", chunk_size=3)
    assert [item["sequence"] for item in chunks] == ["AAC", "CGG", "TT"]
    assert [(item["start"], item["end"]) for item in chunks] == [
        (0, 3), (3, 6), (6, 8)
    ]


def test_chunk_sequence_with_overlap():
    chunks = chunk_sequence("AACCGGTT", chunk_size=4, overlap=1)

    assert [item["sequence"] for item in chunks] == [
        "AACC", "CGGT", "TT"
    ]