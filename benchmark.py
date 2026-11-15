import time
from scheduler import GeneDaskScheduler

TARGET_SECONDS = 180.0  # 3-Minute Goal


def run_benchmark():
  print("Starting benchmark...")
  start_time = time.perf_counter()

  sched = GeneDaskScheduler()
  output = sched.process_genetic_chunks()
  print(f"Computed Result: {output:.4f}")
  #sched.shutdown()

  elapsed_time = time.perf_counter() - start_time

  print("-" * 40)
  print(f"Total Execution Time : {elapsed_time:.2f} seconds")
  print(f"Target Goal          : {TARGET_SECONDS:.2f} seconds")

  if elapsed_time <= TARGET_SECONDS:
    print("STATUS: PASS (3-Minute Goal Achieved!)")
  else:
    print("STATUS: NEEDS OPTIMIZATION (Exceeded 3-Minute Goal)")
  print("-" * 40)


run_benchmark()