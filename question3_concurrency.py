import threading
import time


def fibonacci(n):
    """Return the nth Fibonacci number using an iterative algorithm."""
    if n < 0:
        raise ValueError("n must be zero or greater")
    if n <= 1:
        return n

    previous, current = 0, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current


def run_multithreaded(numbers):
    results = {}
    threads = []

    def calculate(number):
        results[number] = fibonacci(number)

    # Start time is recorded immediately before starting the first thread.
    start_time = time.perf_counter_ns()
    for number in numbers:
        thread = threading.Thread(target=calculate, args=(number,))
        threads.append(thread)
        thread.start()

    # Wait for every thread to finish. The last join completes after the last worker.
    for thread in threads:
        thread.join()
    end_time = time.perf_counter_ns()

    return results, end_time - start_time


def run_sequential(numbers):
    results = {}
    start_time = time.perf_counter_ns()
    for number in numbers:
        results[number] = fibonacci(number)
    end_time = time.perf_counter_ns()
    return results, end_time - start_time


def main():
    numbers = [35, 38, 40]
    rounds = 10
    threaded_times = []
    sequential_times = []

    print("===== FIBONACCI MULTITHREADING EXPERIMENT =====")
    print("Numbers: Fibonacci(35), Fibonacci(38), Fibonacci(40)")
    print(f"Number of rounds: {rounds}\n")

    print("--- Multithreaded Results ---")
    for round_number in range(1, rounds + 1):
        results, elapsed = run_multithreaded(numbers)
        threaded_times.append(elapsed)
        print(f"Round {round_number:2}: {results} | Total time: {elapsed:,} ns")

    threaded_average = sum(threaded_times) / rounds
    print(f"Multithreaded average: {threaded_average:,.2f} ns")

    print("\n--- Sequential Results (No Multithreading) ---")
    for round_number in range(1, rounds + 1):
        results, elapsed = run_sequential(numbers)
        sequential_times.append(elapsed)
        print(f"Round {round_number:2}: {results} | Total time: {elapsed:,} ns")

    sequential_average = sum(sequential_times) / rounds
    print(f"Sequential average:    {sequential_average:,.2f} ns")

    print("\n--- Comparison ---")
    if threaded_average < sequential_average:
        print("Multithreading was faster on average in this experiment.")
    elif threaded_average > sequential_average:
        print("Sequential processing was faster on average in this experiment.")
    else:
        print("Both methods had almost equal average times.")


if __name__ == "__main__":
    main()
