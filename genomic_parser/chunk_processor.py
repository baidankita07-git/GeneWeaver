
"""Generate and attach metadata to genomic sequence chunks."""

from typing import Dict, List


def calculate_gc_content(sequence: str) -> float:
    """Calculate the percentage of G and C nucleotides."""
    if not sequence:
        return 0.0

    sequence = sequence.upper()

    gc_count = sequence.count("G") + sequence.count("C")

    return round((gc_count / len(sequence)) * 100, 2)


def count_nucleotides(sequence: str) -> Dict[str, int]:
    """Count the occurrences of A, T, G and C."""
    sequence = sequence.upper()

    return {
        "A": sequence.count("A"),
        "T": sequence.count("T"),
        "G": sequence.count("G"),
        "C": sequence.count("C"),
    }


def add_chunk_metadata(
    chunks: List[Dict],
    sequence_id: str,
) -> List[Dict]:
    """Add useful genomic information to each sequence chunk.

    Each chunk receives:
        sequence_id: ID of the original genomic sequence.
        gc_content: Percentage of G and C bases.
        nucleotide_counts: Number of A, T, G and C bases.

    The original chunk dictionaries are not modified.
    """

    if not isinstance(chunks, list):
        raise TypeError("Chunks must be provided as a list.")

    if not isinstance(sequence_id, str) or not sequence_id.strip():
        raise ValueError("Please provide a valid sequence ID.")

    enriched_chunks = []

    for chunk in chunks:

        if not isinstance(chunk, dict):
            raise TypeError("Each chunk must be a dictionary.")

        required_fields = [
            "sequence",
            "chunk_index",
            "start",
            "end",
            "length",
        ]

        for field in required_fields:
            if field not in chunk:
                raise ValueError(f"Missing chunk information: {field}")

        sequence = chunk["sequence"]

        if not isinstance(sequence, str):
            raise TypeError("Chunk sequence must be a string.")

        if not isinstance(chunk["start"], int) or not isinstance(chunk["end"], int):
            raise TypeError("Chunk coordinates must be integers.")

        if chunk["start"] < 0 or chunk["end"] < chunk["start"]:
            raise ValueError("Invalid chunk coordinates.")

        if chunk["length"] != len(sequence):
            raise ValueError("Chunk length does not match sequence length.")

        if chunk["end"] - chunk["start"] != chunk["length"]:
            raise ValueError("Chunk coordinates do not match its length.")

        # Calculate metadata for the current chunk.
        metadata = {
            "sequence_id": sequence_id,
            "gc_content": calculate_gc_content(sequence),
            "nucleotide_counts": count_nucleotides(sequence),
        }

        # Combine existing chunk information with new metadata.
        enriched_chunk = {
            **chunk,
            **metadata,
        }

        enriched_chunks.append(enriched_chunk)

    return enriched_chunks
