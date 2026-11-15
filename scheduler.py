import gc
import dask.array as da
import numpy as np
from dask.distributed import Client, LocalCluster
from engine.gpu_aligner import run_dask_chunk


class GeneDaskScheduler:
    """Handles chunked parallel CRISPR alignment across genetic sequences using Dask + CUDA."""

    def _init_(self, n_workers: int = 2, threads_per_worker: int = 2, memory_limit: str = "2GB"):
        self.cluster = LocalCluster(
            n_workers=n_workers,
            threads_per_worker=threads_per_worker,
            memory_limit=memory_limit,
        )
        self.client = Client(self.cluster)

    def align_genome_chunks(
        self,
        genome: np.ndarray,
        grna: np.ndarray,
        chunk_size: int = 1_000_000,
        max_mismatches: int = 3,
    ) -> np.ndarray:
        """Splits a 1D uint8 DNA sequence into memory-safe Dask chunks with overlap,
        runs Member 1's CUDA kernel on each chunk, and returns all mismatch counts.
        """
        overlap_len = len(grna) - 1
        dask_genome = da.from_array(genome, chunks=chunk_size)

        # map_overlap prevents missing off-target matches that straddle chunk boundaries
        aligned_chunks = dask_genome.map_overlap(
            run_dask_chunk,
            depth={0: overlap_len},
            boundary="none",
            trim=True,
            dtype=np.int32,
            grna=grna,
            max_mismatches=max_mismatches,
        )

        results = aligned_chunks.compute()
        gc.collect()
        return results

    def shutdown(self):
        """Safely closes active Dask client or cluster resources if initialized."""
        if hasattr(self, "client") and self.client:
            self.client.close()
        if hasattr(self, "cluster") and self.cluster:
            self.cluster.close()