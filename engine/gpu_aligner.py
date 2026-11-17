import numpy as np
from numba import cuda, int32, uint8

MAX_GRNA_LEN = 32  # Supports standard 20-23bp CRISPR gRNAs with PAM


# WEEK 2 KERNEL: Global VRAM Implementation
@cuda.jit
def _cuda_global_kernel(genome, grna, max_mismatches, results):
    idx = cuda.grid(1)
    m = grna.shape[0]

    if idx <= genome.shape[0] - m:
        mismatches = 0
        for j in range(m):
            if genome[idx + j] != grna[j]:
                mismatches += 1
                if mismatches > max_mismatches:
                    results[idx] = -1
                    return
        results[idx] = mismatches


# WEEK 4 KERNEL: On-Chip CUDA Shared Memory Optimization
@cuda.jit
def _cuda_shared_kernel(genome, grna, max_mismatches, results):
    shared_grna = cuda.shared.array(shape=MAX_GRNA_LEN, dtype=uint8)

    tx = cuda.threadIdx.x
    idx = cuda.grid(1)
    m = grna.shape[0]

    # Cooperatively load gRNA from global VRAM into fast shared memory
    if tx < m:
        shared_grna[tx] = grna[tx]
    cuda.syncthreads()

    if idx <= genome.shape[0] - m:
        mismatches = 0
        for j in range(m):
            if genome[idx + j] != shared_grna[j]:
                mismatches += 1
                if mismatches > max_mismatches:
                    results[idx] = -1
                    return
        results[idx] = mismatches


def gpu_crispr_align(
    genome: np.ndarray,
    grna: np.ndarray,
    max_mismatches: int = 3,
    use_shared_memory: bool = True,
) -> np.ndarray:
    """
    Host wrapper called by Member 2's Dask scheduler.
    Transfers arrays to GPU VRAM, executes the CUDA kernel, and returns mismatch counts.
    """
    if len(grna) > MAX_GRNA_LEN:
        raise ValueError(f"gRNA length cannot exceed {MAX_GRNA_LEN} base pairs.")

    num_positions = len(genome) - len(grna) + 1
    if num_positions <= 0:
        return np.array([], dtype=np.int32)

    # 1. Host (CPU RAM) -> Device (GPU VRAM)
    d_genome = cuda.to_device(np.ascontiguousarray(genome, dtype=np.uint8))
    d_grna = cuda.to_device(np.ascontiguousarray(grna, dtype=np.uint8))
    d_results = cuda.device_array(num_positions, dtype=np.int32)

    # 2. Configure Grid & Block dimensions
    threads_per_block = 256
    blocks_per_grid = (
        num_positions + (threads_per_block - 1)
    ) // threads_per_block

    # 3. Launch Kernel
    if use_shared_memory:
        _cuda_shared_kernel[blocks_per_grid, threads_per_block](
            d_genome, d_grna, max_mismatches, d_results
        )
    else:
        _cuda_global_kernel[blocks_per_grid, threads_per_block](
            d_genome, d_grna, max_mismatches, d_results
        )

    cuda.synchronize()

    # 4. Device (GPU VRAM) -> Host (CPU RAM)
    return d_results.copy_to_host()


def get_gpu_stats() -> dict:
    """
    Telemetry helper for Member 4's Textual TUI dashboard.
    Returns device name and live VRAM usage in megabytes.
    """
    if not cuda.is_available():
        return {
            "available": False,
            "device": "CPU Only",
            "used_mb": 0.0,
            "total_mb": 0.0,
        }

    device = cuda.get_current_device()
    free_bytes, total_bytes = cuda.current_context().get_memory_info()
    used_bytes = total_bytes - free_bytes

    return {
        "available": True,
        "device": device.name.decode("utf-8")
        if isinstance(device.name, bytes)
        else str(device.name),
        "used_mb": round(used_bytes / (1024**2), 2),
        "total_mb": round(total_bytes / (1024**2), 2),
    }
def run_dask_chunk(
    genome_chunk: np.ndarray, grna: np.ndarray, max_mismatches: int = 3
) -> np.ndarray:
    """
    Dask-compatible chunk processor for GeneDaskScheduler.
    Runs the 411x Shared Memory CUDA kernel on GPU, with automatic CPU fallback.
    """
    if len(genome_chunk) < len(grna):
        return np.array([], dtype=np.int32)

    if cuda.is_available():
        return gpu_crispr_align(
            genome=genome_chunk,
            grna=grna,
            max_mismatches=max_mismatches,
            use_shared_memory=True,
        )
    else:
        from .cpu_baseline import cpu_crispr_align

        return cpu_crispr_align(genome_chunk, grna, max_mismatches)
def count_off_target_hits(
    alignment_results: np.ndarray, max_mismatches: int = 3
) -> int:
    """
    Safely counts valid off-target CRISPR hits (0 to max_mismatches),
    excluding -1 sentinel values returned for non-matching positions.
    """
    valid_mask = (alignment_results >= 0) & (
        alignment_results <= max_mismatches
    )
    return int(np.sum(valid_mask))
def extract_hit_indices(
    alignment_results: np.ndarray, max_mismatches: int = 3
) -> np.ndarray:
    """ Returns exact genomic indices where valid off-target matches occur,
    ready for Member 3's CRISPR PAM scoring and Member 4's TUI viewer."""
    return np.where(
        (alignment_results >= 0) & (alignment_results <= max_mismatches)
    )[0]
