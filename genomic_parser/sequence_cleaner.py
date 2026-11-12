"""DNA sequence normalization and cleaning."""

from .sequence_validator import validate_dna_sequence


def clean_dna_sequence(
    sequence: str,
    allow_ambiguous: bool = True,
    remove_whitespace: bool = True,
) -> str:
    """Uppercase a DNA sequence, optionally remove whitespace, then validate."""
    if not isinstance(sequence, str):
        raise TypeError("sequence must be a string")

    cleaned = sequence.upper()
    if remove_whitespace:
        cleaned = "".join(cleaned.split())
    elif any(char.isspace() for char in cleaned):
        raise ValueError("Whitespace found; set remove_whitespace=True to remove it")

    validate_dna_sequence(cleaned, allow_ambiguous=allow_ambiguous)
    return cleaned
