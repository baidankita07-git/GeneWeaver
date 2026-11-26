"""Detect nucleotide mismatches in CRISPR guide-target sequences."""

from typing import Dict, List


def detect_mismatches(
    guide_sequence: str,
    target_sequence: str,
) -> Dict:
    """Identify mismatches between guide RNA and target DNA.

    RNA nucleotide U is converted to DNA nucleotide T before comparison.

    Args:
        guide_sequence: CRISPR guide RNA sequence.
        target_sequence: Target DNA sequence.

    Returns:
        Dictionary containing:
            mismatch_count: Total number of mismatches.
            matching_count: Total matching positions.
            mismatch_positions: Details of each mismatch.
            matching_positions: Positions with matching bases.
            is_perfect_match: True if no mismatches exist.

    Raises:
        TypeError: If inputs are not strings.
        ValueError: If sequences are empty, invalid, or unequal in length.
    """

    if not isinstance(guide_sequence, str):
        raise TypeError("Guide sequence must be a string.")

    if not isinstance(target_sequence, str):
        raise TypeError("Target sequence must be a string.")

    guide = "".join(guide_sequence.upper().split())
    target = "".join(target_sequence.upper().split())

    if not guide or not target:
        raise ValueError("Guide and target sequences cannot be empty.")

    if set(guide) - {"A", "U", "G", "C"}:
        raise ValueError("Guide must contain only A, U, G and C.")

    if set(target) - {"A", "T", "G", "C"}:
        raise ValueError("Target must contain only A, T, G and C.")

    if len(guide) != len(target):
        raise ValueError("Guide and target lengths must be equal.")

    # Convert RNA notation into DNA notation.
    guide = guide.replace("U", "T")

    mismatch_positions: List[Dict] = []
    matching_positions = []

    for index, (guide_base, target_base) in enumerate(
        zip(guide, target)
    ):
        if guide_base != target_base:
            mismatch_positions.append({
                "position": index,
                "guide_base": guide_base,
                "target_base": target_base,
            })
        else:
            matching_positions.append(index)

    mismatch_count = len(mismatch_positions)
    matching_count = len(matching_positions)

    return {
        "mismatch_count": mismatch_count,
        "matching_count": matching_count,
        "mismatch_positions": mismatch_positions,
        "matching_positions": matching_positions,
        "is_perfect_match": mismatch_count == 0,
    }
