
"""Extract metadata from genomic DNA sequences."""

from typing import Dict


def extract_sequence_metadata(sequence: str) -> Dict:
    """Calculate basic metadata for a genomic DNA sequence.

    Args:
        sequence: DNA sequence represented as a string.

    Returns:
        Dictionary containing:
            length: Total number of bases.
            nucleotide_counts: Count of A, T, G, and C.
            gc_content: GC percentage.
            ambiguous_bases: Number of non-ATGC characters.

    Raises:
        TypeError: If sequence is not a string.
        ValueError: If sequence is empty.
    """
    if not isinstance(sequence, str):
        raise TypeError("sequence must be a string")

    sequence = sequence.upper()

    if not sequence:
        raise ValueError("sequence cannot be empty")

    nucleotide_counts = {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "G": sequence.count("G"),
        "C": sequence.count("C"),
    }

    length = len(sequence)

    gc_count = nucleotide_counts["G"] + nucleotide_counts["C"]

    gc_content = (gc_count / length) * 100

    ambiguous_bases = length - sum(nucleotide_counts.values())

    return {
        "length": length,
        "nucleotide_counts": nucleotide_counts,
        "gc_content": round(gc_content, 2),
        "ambiguous_bases": ambiguous_bases,
    }
