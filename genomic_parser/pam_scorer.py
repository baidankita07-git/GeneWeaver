
"""Calculate PAM-aware scores for CRISPR target sequences."""

from typing import Dict


def calculate_pam_aware_score(
    mismatch_score: float,
    pam_sequence: str,
    pam_pattern: str = "NGG",
    invalid_pam_penalty: float = 100.0,
) -> Dict:
    """Combine mismatch penalties with PAM recognition.

    N in the PAM pattern represents any valid DNA nucleotide.

    Args:
        mismatch_score: Total mismatch penalty from position_scorer.
        pam_sequence: PAM sequence identified in the target.
        pam_pattern: Expected PAM pattern, default is NGG.
        invalid_pam_penalty: Penalty assigned when PAM is invalid.

    Returns:
        PAM validity and combined scoring information.
    """

    if not isinstance(mismatch_score, (int, float)):
        raise TypeError("Mismatch score must be numeric.")

    if mismatch_score < 0:
        raise ValueError("Mismatch score cannot be negative.")

    if not isinstance(pam_sequence, str) or not isinstance(pam_pattern, str):
        raise TypeError("PAM sequence and pattern must be strings.")

    if not isinstance(invalid_pam_penalty, (int, float)):
        raise TypeError("Invalid PAM penalty must be numeric.")

    if invalid_pam_penalty < 0:
        raise ValueError("Invalid PAM penalty cannot be negative.")

    pam = "".join(pam_sequence.upper().split())
    pattern = "".join(pam_pattern.upper().split())

    if not pam or not pattern:
        raise ValueError("PAM sequence and pattern cannot be empty.")

    valid_bases = {"A", "T", "G", "C"}

    if set(pam) - valid_bases:
        raise ValueError("PAM sequence must contain only A, T, G and C.")

    if set(pattern) - (valid_bases | {"N"}):
        raise ValueError("PAM pattern supports only A, T, G, C and N.")

    if len(pam) != len(pattern):
        raise ValueError("PAM sequence and pattern must have equal lengths.")

    pam_is_valid = all(
        expected == "N" or expected == actual
        for actual, expected in zip(pam, pattern)
    )

    if pam_is_valid:
        total_score = float(mismatch_score)
    else:
        total_score = float(mismatch_score) + float(invalid_pam_penalty)

    return {
        "pam_sequence": pam,
        "pam_pattern": pattern,
        "pam_valid": pam_is_valid,
        "mismatch_score": round(float(mismatch_score), 2),
        "pam_penalty": 0.0 if pam_is_valid else float(invalid_pam_penalty),
        "total_score": round(total_score, 2),
    }
