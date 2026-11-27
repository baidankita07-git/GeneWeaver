import numpy as np
from engine.cpu_baseline import cpu_crispr_align
from engine.gpu_aligner import count_off_target_hits, extract_hit_indices, recommend_chunk_size


def test_engine_helpers():
    genome = np.array([0, 1, 2, 3, 0, 1, 2, 3, 0, 1], dtype=np.uint8)
    grna = np.array([0, 1, 2, 3], dtype=np.uint8)
    res = cpu_crispr_align(genome, grna, max_mismatches=0)

    assert count_off_target_hits(res, max_mismatches=0) == 2
    assert list(extract_hit_indices(res, max_mismatches=0)) == [0, 4]
    assert recommend_chunk_size() >= 100_000
    print("All engine unit tests passed!")


if _name_ == "_main_":
    test_engine_helpers()
