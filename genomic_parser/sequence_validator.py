
"""Validate DNA sequences for the GeneWeaver project."""

from typing import Dict


VALID_DNA_BASES = {"A", "T", "G", "C"}


def validate_dna_sequence(sequence: str) -> Dict:
    """Validate a DNA sequence and report invalid characters.

    Args:
        sequence: DNA sequence represented as a string.

    Returns:
        Dictionary containing:
            is_valid: Whether the sequence contains only valid DNA bases.
            length: Total sequence length.
            invalid_bases: Sorted list of invalid characters.
            invalid_count: Number of invalid characters.

    Raises:
        TypeError: If sequence is not a string.
        ValueError: If sequence is empty.
    """
    if not isinstance(sequence, str):
        raise TypeError("sequence must be a string")

    sequence = sequence.upper()

    if not sequence:
        raise ValueError("DNA sequence cannot be empty")

    invalid_bases = sorted(set(sequence) - VALID_DNA_BASES)

    invalid_count = sum(
        base not in VALID_DNA_BASES for base in sequence
    )

    return {
        "is_valid": invalid_count == 0,
        "length": len(sequence),
        "invalid_bases": invalid_bases,
        "invalid_count": invalid_count,
    }


def is_valid_dna_sequence(sequence: str) -> bool:
    """Return True if the DNA sequence contains only A, T, G and C."""
    return validate_dna_sequence(sequence)["is_valid"]
