
"""Split long genomic sequences into indexed chunks."""

from typing import Dict, List


def chunk_sequence(sequence: str, chunk_size: int, overlap: int = 0) -> List[Dict]:
    """Split a sequence into chunks with zero-based, half-open coordinates.

    Each result includes sequence, chunk_index, start, end and length.
    Adjacent chunks overlap by the requested number of bases.
    Coordinates always reference the original sequence.
    """
    if not isinstance(sequence, str):
        raise TypeError("sequence must be a string")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

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


def chunk_genome(records: list, chunk_size: int, overlap: int = 0) -> List[Dict]:
    """Chunk FASTA dictionaries returned by read_fasta, preserving record IDs."""
    output = []

    for record in records:
        for chunk in chunk_sequence(record["sequence"], chunk_size, overlap):
            output.append({
                "sequence_id": record["id"],
                **chunk,
            })

    return output
