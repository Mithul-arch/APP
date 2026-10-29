import queue
import random
import threading
import time

results = {}                      
results_lock = threading.Lock()
stop_event = threading.Event()     


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] [{threading.current_thread().name}] {msg}")

def count_primes(limit: int) -> None:
    log(f"Counting primes below {limit}...")
    count = 0
    for n in range(2, limit):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            count += 1
    with results_lock:
        results["primes"] = count
    log(f"Done: {count} primes found")


def download_file(name: str, seconds: float) -> None:
    log(f"Downloading {name}...")
    time.sleep(seconds)            
    with results_lock:
        results[f"download:{name}"] = f"{random.randint(100, 999)} KB"
    log(f"Finished {name}")


SENTINEL = None


def producer(q: queue.Queue, n_items: int) -> None:
    for i in range(1, n_items + 1):
        time.sleep(random.uniform(0.1, 0.3))
        q.put(i)
        log(f"Produced item {i}")
    q.put(SENTINEL)               


def consumer(q: queue.Queue) -> None:
    total = 0
    while True:
        item = q.get()
        if item is SENTINEL:
            break
        total += item ** 2
        log(f"Consumed item {item}")
        q.task_done()
    with results_lock:
        results["sum_of_squares"] = total
    log(f"Consumer finished, sum of squares = {total}")


def heartbeat(interval: float) -> None:
    beats = 0
    while not stop_event.wait(interval):   
        beats += 1
        log(f"♥ heartbeat #{beats}")


def main() -> None:
    start = time.perf_counter()
    q = queue.Queue()

    monitor = threading.Thread(target=heartbeat, args=(0.5,), name="Monitor", daemon=True)

    workers = [
        threading.Thread(target=count_primes, args=(200_000,), name="PrimeWorker"),
        threading.Thread(target=download_file, args=("report.pdf", 1.2), name="Download-1"),
        threading.Thread(target=download_file, args=("data.csv", 0.8), name="Download-2"),
        threading.Thread(target=producer, args=(q, 6), name="Producer"),
        threading.Thread(target=consumer, args=(q,), name="Consumer"),
    ]

    monitor.start()
    for t in workers:
        t.start()

    for t in workers:          
        t.join()

    stop_event.set()              
    monitor.join()

    print("\n=== Results ===")
    for key, value in sorted(results.items()):
        print(f"{key:>20}: {value}")
    print(f"\nTotal elapsed: {time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    main()