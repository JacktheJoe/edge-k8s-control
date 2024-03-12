limit = 10000

def compute_fibonacci(limit):
    fib_numbers = [0, 1]
    while True:
        next_fib = fib_numbers[-1] + fib_numbers[-2]
        if next_fib > limit:
            break
        fib_numbers.append(next_fib)
    return fib_numbers

fibonacci_sequence = compute_fibonacci(limit)
print(f"Fibonacci numbers up to {limit}: {fibonacci_sequence}")
