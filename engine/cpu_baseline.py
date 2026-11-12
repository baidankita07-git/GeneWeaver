import numpy as np
def cpu_crispr_align(
    genome: np.ndarray, grna: np.ndarray, max_mismatches: int = 3
) -> np.ndarray:
    n = len(genome)
    m = len(grna)
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
