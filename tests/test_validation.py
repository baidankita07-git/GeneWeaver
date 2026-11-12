import pytest
from genomic_parser.sequence_validator import (
    validate_dna_sequence, is_valid_dna_sequence
)
from genomic_parser.sequence_cleaner import clean_dna_sequence


def test_validation_accepts_canonical_and_ambiguous():
    validate_dna_sequence("ACGT")
    validate_dna_sequence("ACGTN")


def test_validation_rejects_invalid_symbol():
    with pytest.raises(ValueError):
        validate_dna_sequence("ACGTX")


def test_canonical_only_validation():
    assert not is_valid_dna_sequence("ACGTN", allow_ambiguous=False)


def test_cleaning_uppercases_and_removes_whitespace():
    assert clean_dna_sequence(" ac gt\n") == "ACGT"
