import time
from cpu_baseline import cpu_crispr_align
from gpu_aligner import gpu_crispr_align
from numba import cuda
import numpy as np


def run_benchmark(genome_size: int = 2_000_000, grna_len: int = 23):
    print(f"--- GeneWeaver Member 1 Benchmark ({genome_size:,} base pairs) ---")

    # Generate mock encoded DNA (0=A, 1=C, 2=G, 3=T)
    rng = np.random.default_rng(42)
    genome = rng.integers(0, 4, size=genome_size, dtype=np.uint8)
    grna = rng.integers(0, 4, size=grna_len, dtype=np.uint8)

    # Inject an exact match at index 500 to verify detection
    genome[500 : 500 + grna_len] = grna

    # 1. Time Pure Python CPU Baseline
    start_cpu = time.perf_counter()
    cpu_out = cpu_crispr_align(genome, grna, max_mismatches=3)
    cpu_time = time.perf_counter() - start_cpu
    print(f"CPU Baseline Time:        {cpu_time:.4f} seconds")

    if not cuda.is_available():
        print("No Nvidia GPU detected on this machine. Skipping CUDA test.")
        return

    # 2. Warm-up JIT compilation (excluded from benchmark timing)
    _ = gpu_crispr_align(genome[:1000], grna, max_mismatches=3)

    # 3. Time CUDA Global Memory Kernel
    start_gpu_global = time.perf_counter()
    gpu_global_out = gpu_crispr_align(
        genome, grna, max_mismatches=3, use_shared_memory=False
    )
    gpu_global_time = time.perf_counter() - start_gpu_global
    print(
        f"GPU Global Kernel Time:   {gpu_global_time:.4f} seconds ({cpu_time / gpu_global_time:.1f}x speedup)"
    )

    # 4. Time CUDA Shared Memory Kernel
    start_gpu_shared = time.perf_counter()
    gpu_shared_out = gpu_crispr_align(
        genome, grna, max_mismatches=3, use_shared_memory=True
    )
    gpu_shared_time = time.perf_counter() - start_gpu_shared
    print(
        f"GPU Shared Kernel Time:   {gpu_shared_time:.4f} seconds ({cpu_time / gpu_shared_time:.1f}x speedup)"
    )

    # 5. Verify Exact Numerical Match
    assert np.array_equal(cpu_out, gpu_global_out), "Global GPU mismatch!"
    assert np.array_equal(cpu_out, gpu_shared_out), "Shared GPU mismatch!"
    print("SUCCESS: GPU outputs match CPU baseline 100%.")


if __name__== "__main__":
    run_benchmark()
