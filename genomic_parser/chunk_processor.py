
"""Split genomic DNA sequences into configurable chunks."""

from typing import Dict, List


def chunk_sequence(
    sequence: str,
    chunk_size: int,
    overlap: int = 0,
) -> List[Dict]:
    """Divide a genomic sequence into overlapping chunks.

    Args:
        sequence: Original genomic DNA sequence.
        chunk_size: Maximum number of bases in each chunk.
        overlap: Number of bases shared between consecutive chunks.

    Returns:
        List of dictionaries containing:
            sequence: Chunk DNA sequence.
            chunk_index: Zero-based chunk index.
            start: Starting position in the original sequence.
            end: Ending position (exclusive).
            length: Number of bases in the chunk.

    Raises:
        TypeError: If sequence is not a string.
        ValueError: If chunk_size or overlap is invalid.
    """
    if not isinstance(sequence, str):
        raise TypeError("sequence must be a string")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size"
        )

    if not sequence:
        return []

    chunks = []
    step = chunk_size - overlap

    for index, start in enumerate(range(0, len(sequence), step)):
        end = min(start + chunk_size, len(sequence))

        chunks.append({
            "sequence": sequence[start:end],
            "chunk_index": index,
            "start": start,
            "end": end,
            "length": end - start,
        })

        if end == len(sequence):
            break

    return chunks
