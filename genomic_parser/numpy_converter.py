"""Convert DNA sequences to and from compact NumPy arrays."""

import numpy as np

# Two-bit encoding for canonical DNA bases.
_BASE_TO_INT = {"A": 0, "C": 1, "G": 2, "T": 3}
_INT_TO_BASE = np.array(["A", "C", "G", "T"])


def encode_dna_sequence(sequence: str, dtype=np.uint8) -> np.ndarray:
    """Encode a canonical A/C/G/T sequence as a one-dimensional NumPy array.

    Ambiguous IUPAC symbols are deliberately rejected because they do not have
    a unique two-bit representation.
    """
    if not isinstance(sequence, str):
        raise TypeError("sequence must be a string")
    normalized = "".join(sequence.split()).upper()
    invalid = sorted(set(normalized) - set(_BASE_TO_INT))
    if invalid:
        raise ValueError(
            "Only A, C, G and T can be encoded; found: " + ", ".join(invalid)
        )
    return np.fromiter((_BASE_TO_INT[base] for base in normalized), dtype=dtype)


def decode_dna_array(encoded: np.ndarray) -> str:
    """Decode an array produced by encode_dna_sequence back to DNA text."""
    values = np.asarray(encoded)
    if values.ndim != 1:
        raise ValueError("encoded sequence must be one-dimensional")
    if values.size and (not np.issubdtype(values.dtype, np.integer)
                        or np.any(values < 0) or np.any(values > 3)):
        raise ValueError("encoded values must be integers in the range 0..3")
    return "".join(_INT_TO_BASE[values.astype(np.intp)].tolist())
