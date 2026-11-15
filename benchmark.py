import time
from scheduler import GeneDaskScheduler

TARGET_SECONDS = 180.0  # 3-Minute Goal


def run_benchmark():
  print("Starting GeneWeaver Dask Benchmark...")
  data_shape = (10000, 1000)
  chunk_size = (1000, 1000)

  start_time = time.perf_counter()

  sched = GeneDaskScheduler()
  output = sched.process_genetic_chunks(
      data_shape=data_shape, chunk_size=chunk_size
  )
  sched.shutdown()

  elapsed_time = time.perf_counter() - start_time

  print("-" * 45)
  print(f"Matrix Shape         : {data_shape}")
  print(f"Chunk Size           : {chunk_size}")
  print(f"Computed Result      : {output:.4f}")
  print(f"Total Execution Time : {elapsed_time:.2f} seconds")
  print(f"Target Goal          : {TARGET_SECONDS:.2f} seconds")

  if elapsed_time <= TARGET_SECONDS:
    print("STATUS: PASS (3-Minute Goal Achieved!)")
  else:
    print("STATUS: NEEDS OPTIMIZATION (Exceeded 3-Minute Goal)")
  print("-" * 45)


run_benchmark()