
"""Tests for FASTA file ingestion."""

import pytest

from genomic_parser.fasta_reader import read_fasta


def test_read_single_fasta_record(tmp_path):
    fasta_file = tmp_path / "single.fasta"
    fasta_file.write_text(
        ">sequence_001 Sample sequence\nATGCGTAC\n",
        encoding="utf-8",
    )

    records = read_fasta(fasta_file)

    assert len(records) == 1
    assert records[0]["id"] == "sequence_001"
    assert records[0]["description"] == "sequence_001 Sample sequence"
    assert records[0]["sequence"] == "ATGCGTAC"
    assert records[0]["length"] == 8


def test_read_multiple_fasta_records(tmp_path):
    fasta_file = tmp_path / "multiple.fa"
    fasta_file.write_text(
        ">seq1 First sequence\nATGC\n"
        ">seq2 Second sequence\nGGTTAA\n",
        encoding="utf-8",
    )

    records = read_fasta(fasta_file)

    assert len(records) == 2
    assert records[0]["id"] == "seq1"
    assert records[1]["id"] == "seq2"
    assert records[0]["sequence"] == "ATGC"
    assert records[1]["sequence"] == "GGTTAA"


def test_sequence_is_converted_to_uppercase(tmp_path):
    fasta_file = tmp_path / "lowercase.fasta"
    fasta_file.write_text(
        ">seq1 Lowercase sequence\natgcgt\n",
        encoding="utf-8",
    )

    records = read_fasta(fasta_file)

    assert records[0]["sequence"] == "ATGCGT"


def test_read_empty_fasta_file(tmp_path):
    fasta_file = tmp_path / "empty.fasta"
    fasta_file.write_text("", encoding="utf-8")

    records = read_fasta(fasta_file)

    assert records == []


def test_missing_fasta_file():
    with pytest.raises(FileNotFoundError):
        read_fasta("data/nonexistent.fasta")


def test_unsupported_file_extension(tmp_path):
    text_file = tmp_path / "sequence.txt"
    text_file.write_text(">seq1\nATGC\n", encoding="utf-8")

    with pytest.raises(ValueError):
        read_fasta(text_file)


def test_directory_instead_of_file(tmp_path):
    with pytest.raises(IsADirectoryError):
        read_fasta(tmp_path)
