import gc
import dask.array as da
import numpy as np


class GeneDaskScheduler:
  """Handles chunked parallel processing of genetic sequence matrices using Dask."""

  def process_genetic_chunks(
      self, data_shape=(10000, 1000), chunk_size=(1000, 1000)
  ):
    """Processes genetic arrays in memory-safe chunks and returns mean score."""
    dask_data = da.random.random(data_shape, chunks=chunk_size)
    processed = dask_data.map_blocks(
        self._safe_chunk_compute, dtype=np.float64
    )
    result = processed.mean().compute()
    gc.collect()
    return float(result)

  @staticmethod
  def _safe_chunk_compute(chunk):
    """Applies vectorized mathematical transformation to an individual chunk."""
    return np.square(chunk) + np.sqrt(chunk)

  def shutdown(self):
    """Safely closes active Dask client or cluster resources if initialized."""
    if hasattr(self, "client") and self.client:
      self.client.close()
    if hasattr(self, "cluster") and self.cluster:
      self.cluster.close()