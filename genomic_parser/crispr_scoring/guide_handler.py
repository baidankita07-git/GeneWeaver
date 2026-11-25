
"""Handle and validate CRISPR guide RNA sequences."""

from typing import Dict


VALID_RNA_BASES = {"A", "U", "G", "C"}


def process_guide_sequence(guide_sequence: str) -> Dict:
    """Normalize and validate a CRISPR guide RNA sequence.

    Args:
        guide_sequence: Raw guide RNA sequence.

    Returns:
        Dictionary containing:
            guide_sequence: Normalized RNA sequence.
            length: Number of nucleotides.
            gc_content: GC percentage.
            nucleotide_counts: Count of A, U, G and C.
            is_valid: Whether the sequence is valid RNA.

    Raises:
        TypeError: If input is not a string.
        ValueError: If the sequence is empty or contains invalid bases.
    """
    if not isinstance(guide_sequence, str):
        raise TypeError("Guide sequence must be a string")

    # Normalize sequence by removing whitespace and converting to uppercase.
    sequence = "".join(guide_sequence.upper().split())

    if not sequence:
        raise ValueError("Guide sequence cannot be empty")

    invalid_bases = sorted(set(sequence) - VALID_RNA_BASES)

    if invalid_bases:
        raise ValueError(
            f"Invalid RNA bases found: {invalid_bases}. "
            "Expected only A, U, G and C."
        )

    nucleotide_counts = {
        base: sequence.count(base)
        for base in "AUGC"
    }

    length = len(sequence)

    gc_count = nucleotide_counts["G"] + nucleotide_counts["C"]

    gc_content = (gc_count / length) * 100

    return {
        "guide_sequence": sequence,
        "length": length,
        "gc_content": round(gc_content, 2),
        "nucleotide_counts": nucleotide_counts,
        "is_valid": True,
    }


def validate_guide_length(
    guide_sequence: str,
    expected_length: int = 20,
) -> bool:
    """Check whether a guide RNA has the expected length.

    Args:
        guide_sequence: Normalized or raw guide RNA sequence.
        expected_length: Expected number of nucleotides.

    Returns:
        True if the guide has the expected length.

    Raises:
        ValueError: If expected_length is not positive.
    """
    if expected_length <= 0:
        raise ValueError("Expected length must be greater than zero")

    processed = process_guide_sequence(guide_sequence)

    return processed["length"] == expected_length
