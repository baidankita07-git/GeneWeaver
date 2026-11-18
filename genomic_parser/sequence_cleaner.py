
"""Clean genomic DNA sequences for the GeneWeaver project."""

from typing import Dict

VALID_DNA_BASES = {"A", "T", "G", "C"}


def clean_dna_sequence(
    sequence: str,
    remove_invalid: bool = False,
) -> Dict:
    """Clean a DNA sequence and report the changes made.

    Args:
        sequence: Raw DNA sequence.
        remove_invalid: If True, remove characters other than A, T, G and C.

    Returns:
        Dictionary containing:
            original_sequence: Original input sequence.
            cleaned_sequence: Processed DNA sequence.
            original_length: Original sequence length.
            cleaned_length: Cleaned sequence length.
            removed_characters: Characters removed during cleaning.
            removed_count: Number of removed characters.

    Raises:
        TypeError: If sequence is not a string.
        ValueError: If the sequence is empty or cleaning removes everything.
    """
    if not isinstance(sequence, str):
        raise TypeError("sequence must be a string")

    if not sequence.strip():
        raise ValueError("DNA sequence cannot be empty")

    original_length = len(sequence)

    # Convert to uppercase and remove whitespace.
    cleaned = "".join(sequence.upper().split())

    removed_characters = []

    if remove_invalid:
        removed_characters = [
            base for base in cleaned
            if base not in VALID_DNA_BASES
        ]

        cleaned = "".join(
            base for base in cleaned
            if base in VALID_DNA_BASES
        )

    if not cleaned:
        raise ValueError("Cleaning removed all sequence characters")

    return {
        "original_sequence": sequence,
        "cleaned_sequence": cleaned,
        "original_length": original_length,
        "cleaned_length": len(cleaned),
        "removed_characters": removed_characters,
        "removed_count": len(removed_characters),
    }
