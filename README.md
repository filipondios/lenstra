# Lenstra

This is a very simple python program (without dependencies) that attempts to find if a number is not prime using the [Lenstra elliptic-curve factorization](https://en.wikipedia.org/wiki/Lenstra_elliptic-curve_factorization) algorithm.
Using Lenstra helps this program purpose: determining if a number is not prime by finding small factors in large composite numbers.

## Usage
Run the program with the required arguments:

```bash
python lenstra.py -n <number> [-i <iterations>] [-v] [-b <base>]
```

### Arguments

| Argument           | Optional                | Description                                                                      |
|--------------------|:-----------------------:|----------------------------------------------------------------------------------|
| `-n, --number`     | :x:                     | The number to test                                                               |
| `-i, --iterations` | :white_check_mark:      | The maximum number of iterations for the algorithm                               |
| `-b, --base`       | :white_check_mark:      | Base of the number to test (binary=bin, octal=oct, decimal=dec, hexadecimal=hex) |
| `-v, --verbose`    | :white_check_mark:      | Enables extra logging for debugging and detailed output                          |

### Example

The following execution will attempt to find factors of `5615377489327409283` (4DEDD4133315C883 in hexadecimal) 
using up to `200` iterations with verbose logging enabled. Note that you can also write the hexadecimal 
digits in lowercase.

```shell
python lenstra.py -n 0x4DEDD4133315C883 -i 200 -v -b hex
```
> [!IMPORTANT]  
> The Lenstra algorithm is probabilistic and may not always find factors within the given iteration limit.
> For large numbers, increasing the iteration count may improve the chance of finding factors.

## References

- [Corbellini, A. (2015, May 17). *Elliptic Curve Cryptography: A Gentle Introduction*](https://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/)
- [RareSkills. (2024, August 26). *Group Theory*](https://www.rareskills.io/post/group-theory)
- [RareSkills. (2023, September 26). *Elliptic Curve Addition*](https://www.rareskills.io/post/elliptic-curve-addition)
- [Dattoli, G., Sabia, E., & Tata, A. (2024). *Mathematics*, 12(6), 881](https://www.mdpi.com/2227-7390/12/6/881)
