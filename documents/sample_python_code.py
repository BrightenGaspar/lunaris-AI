def fibonacci(n: int) -> list[int]:
    """Generates Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]

if __name__ == "__main__":
    print(f"First 10 Fibonacci numbers: {fibonacci(10)}")
