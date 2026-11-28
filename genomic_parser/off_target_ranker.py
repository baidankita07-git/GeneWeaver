
"""Rank potential CRISPR off-target sites by their scores."""

from typing import Dict, List


def rank_off_target_sites(
    candidates: List[Dict],
) -> List[Dict]:
    """Rank off-target candidates from lowest to highest penalty.

    Each candidate must contain:
        site_id: Unique identifier for the target site.
        total_score: PAM-aware penalty score.

    Returns:
        A sorted list containing candidates with their assigned ranks.
    """

    if not isinstance(candidates, list):
        raise TypeError("Candidates must be provided as a list.")

    validated_candidates = []
    seen_ids = set()

    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise TypeError("Each candidate must be a dictionary.")

        if "site_id" not in candidate or "total_score" not in candidate:
            raise ValueError(
                "Each candidate must contain site_id and total_score."
            )

        site_id = candidate["site_id"]
        score = candidate["total_score"]

        if not isinstance(site_id, str) or not site_id.strip():
            raise ValueError("site_id must be a non-empty string.")

        if site_id in seen_ids:
            raise ValueError(f"Duplicate site_id found: {site_id}")

        if isinstance(score, bool) or not isinstance(score, (int, float)):
            raise TypeError("total_score must be numeric.")

        if score < 0:
            raise ValueError("total_score cannot be negative.")

        seen_ids.add(site_id)

        validated_candidates.append(candidate.copy())

    # Lower penalty scores indicate better-ranked candidates.
    ranked_candidates = sorted(
        validated_candidates,
        key=lambda item: item["total_score"]
    )

    for rank, candidate in enumerate(ranked_candidates, start=1):
        candidate["rank"] = rank

    return ranked_candidates
