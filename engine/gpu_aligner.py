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
    # Allocate ultra-fast shared memory for the gRNA sequence inside each block
    shared_grna = cuda.shared.array(shape=MAX_GRNA_LEN, dtype=uint8)

    tx = cuda.threadIdx.x
    idx = cuda.grid(1)
    m = grna.shape[0]

    # Cooperatively load gRNA from slow global VRAM into fast shared memory
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
