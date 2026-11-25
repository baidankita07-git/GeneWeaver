
"""Detect PAM sequences in genomic DNA."""

from typing import Dict, List


VALID_DNA_BASES = {"A", "T", "G", "C"}


def detect_pam_sites(
    sequence: str,
    pam_pattern: str = "NGG",
) -> List[Dict]:
    """Find PAM sites in a DNA sequence.

    Args:
        sequence: Genomic DNA sequence.
        pam_pattern: PAM pattern where N represents any DNA base.

    Returns:
        List of dictionaries containing:
            pam_sequence: Identified PAM sequence.
            start: Zero-based start position.
            end: Zero-based exclusive end position.
            pattern: PAM pattern used.

    Raises:
        TypeError: If inputs are not strings.
        ValueError: If sequence or PAM pattern is invalid.
    """
    if not isinstance(sequence, str):
        raise TypeError("Sequence must be a string")

    if not isinstance(pam_pattern, str):
        raise TypeError("PAM pattern must be a string")

    sequence = "".join(sequence.upper().split())
    pam_pattern = pam_pattern.upper()

    if not sequence:
        raise ValueError("DNA sequence cannot be empty")

    if not pam_pattern:
        raise ValueError("PAM pattern cannot be empty")

    if set(sequence) - VALID_DNA_BASES:
        raise ValueError("Sequence must contain only A, T, G and C")

    if set(pam_pattern) - (VALID_DNA_BASES | {"N"}):
        raise ValueError("PAM pattern may contain only A, T, G, C and N")

    pam_length = len(pam_pattern)
    pam_sites = []

    for start in range(len(sequence) - pam_length + 1):
        candidate = sequence[start:start + pam_length]

        matches = all(
            expected == "N" or expected == actual
            for actual, expected in zip(candidate, pam_pattern)
        )

        if matches:
            pam_sites.append({
                "pam_sequence": candidate,
                "start": start,
                "end": start + pam_length,
                "pattern": pam_pattern,
            })

    return pam_sites
