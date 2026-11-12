"""DNA sequence validation helpers."""

from typing import Iterable

# IUPAC DNA symbols. N denotes any nucleotide; other ambiguity codes are
# accepted by default and can be disabled with allow_ambiguous=False.
VALID_DNA_SYMBOLS = frozenset("ACGT")
AMBIGUOUS_DNA_SYMBOLS = frozenset("RYSWKMBDHVN")
ALL_IUPAC_DNA_SYMBOLS = VALID_DNA_SYMBOLS | AMBIGUOUS_DNA_SYMBOLS


def validate_dna_sequence(
    sequence: str,
    allow_ambiguous: bool = True,
    allow_empty: bool = False,
) -> None:
    """Validate a DNA sequence.

    Returns None for valid input; raises TypeError or ValueError otherwise.
    Whitespace is ignored for validation. Use clean_dna_sequence to normalize it.
    """
    if not isinstance(sequence, str):
        raise TypeError("sequence must be a string")

    normalized = "".join(sequence.split()).upper()
    if not normalized and not allow_empty:
        raise ValueError("DNA sequence must not be empty")

    allowed = ALL_IUPAC_DNA_SYMBOLS if allow_ambiguous else VALID_DNA_SYMBOLS
    invalid = sorted(set(normalized) - allowed)
    if invalid:
        raise ValueError(f"Invalid DNA character(s): {', '.join(invalid)}")


def is_valid_dna_sequence(
    sequence: str,
    allow_ambiguous: bool = True,
    allow_empty: bool = False,
) -> bool:
    """Return True if sequence passes DNA validation; otherwise False."""
    try:
        validate_dna_sequence(sequence, allow_ambiguous, allow_empty)
        return True
    except (TypeError, ValueError):
        return False
