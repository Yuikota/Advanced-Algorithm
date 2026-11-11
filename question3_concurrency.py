import threading
import time


def fibonacci(n):
    # If the number is negative or small, return it directly
    if n < 0:
        return 0
    if n <= 1:
        return n

    # Start loop from 2 up to our target number
    previous, current = 0, 1
    for _ in range(2, n + 1):
        # Shift variables forward to get the next number in the pattern
        previous, current = current, previous + current
    return current


def run_multithreaded(numbers):
    results = {}
    threads = []

    # Small job function for each thread to run
    def calculate(number):
        results[number] = fibonacci(number)

    # Save the time right before starting the threads
    start_time = time.perf_counter_ns()
    for number in numbers:
        # Create a new background worker and start it immediately
        thread = threading.Thread(target=calculate, args=(number,))
        threads.append(thread)
        thread.start()

    # Wait for all workers to finish their jobs
    for thread in threads:
        thread.join()
    end_time = time.perf_counter_ns()

    return results, end_time - start_time


def run_sequential(numbers):
    results = {}
    # Save the time before doing the math normally one by one
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
        print("Result: Multithreading was faster on average.")
    else:
        # It takes extra time to set up threads, which makes it slower for easy math
        print("Result: Sequential processing was faster on average due to thread overhead.")


if __name__ == "__main__":
    main()
