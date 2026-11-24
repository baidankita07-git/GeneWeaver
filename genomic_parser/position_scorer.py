
"""Score CRISPR mismatches based on their positions."""

from typing import Dict, List


def score_mismatches(
    mismatch_positions: List[Dict],
    guide_length: int = 20,
    pam_proximal_weight: float = 2.0,
    pam_distal_weight: float = 1.0,
) -> Dict:
    """Calculate position-based penalties for guide mismatches.

    Position convention:
        Position 0 is the PAM-distal end.
        The final position is the PAM-proximal end.

    Args:
        mismatch_positions: List of mismatch dictionaries containing
            a zero-based 'position' field.
        guide_length: Total guide sequence length.
        pam_proximal_weight: Penalty for PAM-proximal mismatches.
        pam_distal_weight: Penalty for PAM-distal mismatches.

    Returns:
        Dictionary containing individual penalties and total score.
    """

    if not isinstance(guide_length, int) or isinstance(guide_length, bool):
        raise TypeError("Guide length must be an integer.")

    if guide_length <= 0:
        raise ValueError("Guide length must be positive.")

    if pam_proximal_weight < 0 or pam_distal_weight < 0:
        raise ValueError("Mismatch weights cannot be negative.")

    if not isinstance(mismatch_positions, list):
        raise TypeError("Mismatch positions must be a list.")

    scored_mismatches = []
    total_penalty = 0.0

    for mismatch in mismatch_positions:
        if not isinstance(mismatch, dict):
            raise TypeError("Each mismatch must be a dictionary.")

        position = mismatch.get("position")

        if not isinstance(position, int) or isinstance(position, bool):
            raise TypeError("Mismatch position must be an integer.")

        if position < 0 or position >= guide_length:
            raise ValueError("Mismatch position is outside guide length.")

        # Divide the guide into distal and proximal regions.
        midpoint = guide_length / 2

        if position < midpoint:
            region = "PAM-distal"
            penalty = pam_distal_weight
        else:
            region = "PAM-proximal"
            penalty = pam_proximal_weight

        scored_mismatches.append({
            "position": position,
            "region": region,
            "penalty": penalty,
        })

        total_penalty += penalty

    return {
        "guide_length": guide_length,
        "mismatch_count": len(scored_mismatches),
        "scored_mismatches": scored_mismatches,
        "total_penalty": round(total_penalty, 2),
    }
