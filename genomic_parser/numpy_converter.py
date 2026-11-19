
"""Convert genomic DNA sequences into NumPy arrays."""

import numpy as np


# Numerical encoding for DNA nucleotides.
NUCLEOTIDE_MAP = {
    "A": 0,
    "T": 1,
    "G": 2,
    "C": 3,
}

REVERSE_NUCLEOTIDE_MAP = {
    value: key for key, value in NUCLEOTIDE_MAP.items()
}


def encode_dna_sequence(sequence: str) -> np.ndarray:
    """Convert a DNA sequence into a numerical NumPy array.

    Args:
        sequence: DNA sequence containing A, T, G and C.

    Returns:
        NumPy array containing encoded nucleotide values.

    Raises:
        TypeError: If sequence is not a string.
        ValueError: If sequence is empty or contains invalid bases.
    """
    if not isinstance(sequence, str):
        raise TypeError("sequence must be a string")

    sequence = sequence.upper()

    if not sequence:
        raise ValueError("DNA sequence cannot be empty")

    invalid_bases = sorted(set(sequence) - set(NUCLEOTIDE_MAP))

    if invalid_bases:
        raise ValueError(
            f"Invalid DNA bases found: {invalid_bases}"
        )

    encoded_sequence = [
        NUCLEOTIDE_MAP[base] for base in sequence
    ]

    return np.array(encoded_sequence, dtype=np.uint8)


def decode_dna_array(encoded_sequence: np.ndarray) -> str:
    """Convert a numerical NumPy array back into a DNA sequence.

    Args:
        encoded_sequence: NumPy array containing encoded bases.

    Returns:
        Original DNA sequence as a string.

    Raises:
        TypeError: If input is not a NumPy array.
        ValueError: If array is empty or contains invalid values.
    """
    if not isinstance(encoded_sequence, np.ndarray):
        raise TypeError("encoded_sequence must be a NumPy array")

    if encoded_sequence.size == 0:
        raise ValueError("Encoded sequence cannot be empty")

    decoded_bases = []

    for value in encoded_sequence.flat:
        base = REVERSE_NUCLEOTIDE_MAP.get(int(value))

        if base is None:
            raise ValueError(
                f"Invalid encoded nucleotide value: {value}"
            )

        decoded_bases.append(base)

    return "".join(decoded_bases)
