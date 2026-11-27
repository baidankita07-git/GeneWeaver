import time
import numpy as np
from scheduler import GeneDaskScheduler


def run_dask_benchmark():
    print("Initializing GeneDaskScheduler...")
    scheduler = GeneDaskScheduler()

    try:
        # 50 Million base pairs ka dummy DNA genome (0=A, 1=C, 2=G, 3=T as uint8)
        genome_size = 50_000_000
        grna_length = 20
        chunk_size = 1_000_000

        print(f"Generating synthetic genome ({genome_size:,} bp) and {grna_length}bp gRNA...")
        rng = np.random.default_rng(seed=42)
        genome = rng.integers(0, 4, size=genome_size, dtype=np.uint8)
        grna = rng.integers(0, 4, size=grna_length, dtype=np.uint8)

        print("Running chunked Dask + GPU/CPU CRISPR alignment...")
        start_time = time.perf_counter()

        results = scheduler.align_genome_chunks(
            genome=genome,
            grna=grna,
            chunk_size=chunk_size,
            max_mismatches=3,
        )

        elapsed_time = time.perf_counter() - start_time
        valid_matches = np.sum((results >= 0) & (results <= 3))

        print("-" * 50)
        print("Benchmark Complete! (Zero CUDA_OUT_OF_MEMORY errors)")
        print(f"Total Positions Processed : {len(results):,}")
        print(f"Off-Target Matches (<=3)  : {valid_matches:,}")
        print(f"Total Execution Time      : {elapsed_time:.2f} seconds")
        print("-" * 50)

    finally:
        scheduler.shutdown()
        print("Dask cluster shut down cleanly.")


if __name__ == "__main__":
    run_dask_benchmark()
