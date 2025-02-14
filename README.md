# Lenstra

This python program attempts to find non-trivial factors of a given number using the [Lenstra elliptic-curve factorization](https://en.wikipedia.org/wiki/Lenstra_elliptic-curve_factorization) algorithm. This algorithm is particularly effective for finding small factors of large composite numbers.

## Usage
Run the program with the required arguments:

```bash
python lenstra.py -n <number> [-i <iterations>] [-v]
```

### Arguments:
- `-n, --number` (required): The number to test.
- `-i, --iterations` (optional, default=100): The maximum number of iterations for the algorithm.
- `-v, --verbose` (optional): Enables extra logging for debugging and detailed output.

### Example:
```bash
python lenstra.py -n 56153 -i 200 -v
```
This will attempt to find factors of `56153` using up to `200` iterations with verbose logging enabled.

> [!IMPORTANT]  
> The Lenstra algorithm is probabilistic and may not always find factors within the given iteration limit.
> For large numbers, increasing the iteration count may improve the chance of finding factors.

## Requirements
This program does not require external packages as dependencies.
