import numpy as np


def cpu_crispr_align(
    genome: np.ndarray, grna: np.ndarray, max_mismatches: int = 3
) -> np.ndarray:
    """
    Week 1 Baseline: Pure Python sequence alignment to detect CRISPR off-target sites.
    Returns an array of mismatch counts (-1 where mismatches exceed max_mismatches).
    """
    if not isinstance(genome, np.ndarray) or not isinstance(grna, np.ndarray):
        raise TypeError("Both genome and grna must be NumPy arrays.")
    if genome.ndim != 1 or grna.ndim != 1:
        raise ValueError("Both genome and grna must be 1D arrays.")
    if len(grna) == 0:
        raise ValueError("gRNA sequence cannot be empty.")
    if max_mismatches < 0:
        raise ValueError("max_mismatches cannot be negative.")

    n = len(genome)
    m = len(grna)
    if n < m:
        return np.array([], dtype=np.int32)

    num_positions = n - m + 1
    results = np.full(num_positions, -1, dtype=np.int32)

    for i in range(num_positions):
        mismatches = 0
        for j in range(m):
            if genome[i + j] != grna[j]:
                mismatches += 1
                if mismatches > max_mismatches:
                    break
        if mismatches <= max_mismatches:
            results[i] = mismatches

    return results
