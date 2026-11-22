
try:
    from .cpu_baseline import cpu_crispr_align
    from .gpu_aligner import (
        count_off_target_hits,
        extract_hit_indices,
        get_gpu_stats,
        gpu_crispr_align,
        recommend_chunk_size,
        run_dask_chunk,
    )
except ImportError:
    from cpu_baseline import cpu_crispr_align
    from gpu_aligner import (
        count_off_target_hits,
        extract_hit_indices,
        get_gpu_stats,
        gpu_crispr_align,
        recommend_chunk_size,
        run_dask_chunk,
    )

__all__ = [
    "cpu_crispr_align",
    "gpu_crispr_align",
    "run_dask_chunk",
    "get_gpu_stats",
    "count_off_target_hits",
    "extract_hit_indices",
    "recommend_chunk_size",
]
