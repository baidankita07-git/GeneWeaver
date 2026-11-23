
"""Attach and preserve metadata for genomic sequence chunks."""

from typing import Dict, List


def add_chunk_metadata(
    chunks: List[Dict],
    sequence_id: str,
) -> List[Dict]:
    """Add metadata to genomic chunks without modifying the originals.

    Args:
        chunks: List of chunks produced by chunk_sequence().
        sequence_id: Identifier of the original genomic sequence.

    Returns:
        A new list of chunks containing additional metadata.

    Raises:
        TypeError: If inputs have incorrect types.
        ValueError: If sequence_id is empty or chunk metadata is invalid.
    """
    if not isinstance(chunks, list):
        raise TypeError("chunks must be a list")

    if not isinstance(sequence_id, str):
        raise TypeError("sequence_id must be a string")

    if not sequence_id.strip():
        raise ValueError("sequence_id cannot be empty")

    enriched_chunks = []

    for chunk in chunks:
        if not isinstance(chunk, dict):
            raise TypeError("Each chunk must be a dictionary")

        required_fields = {
            "sequence", "chunk_index", "start", "end", "length"
        }

        missing_fields = required_fields - chunk.keys()

        if missing_fields:
            raise ValueError(
                f"Chunk is missing fields: {sorted(missing_fields)}"
            )

        sequence = chunk["sequence"]

        if not isinstance(sequence, str):
            raise TypeError("Chunk sequence must be a string")

        if chunk["length"] != len(sequence):
            raise ValueError("Chunk length does not match sequence length")

        if chunk["end"] - chunk["start"] != chunk["length"]:
            raise ValueError("Chunk coordinates do not match its length")

        gc_count = sequence.upper().count("G") + sequence.upper().count("C")

        nucleotide_counts = {
            base: sequence.upper().count(base)
            for base in "ATGC"
        }

        metadata = {
            "sequence_id": sequence_id,
            "gc_content": round(
                (gc_count / len(sequence)) * 100, 2
            ) if sequence else 0.0,
            "nucleotide_counts": nucleotide_counts,
        }

        enriched_chunks.append({
            **chunk,
            **metadata,
        })

    return enriched_chunks
