# Lenstra

This is a very simple python program (without dependencies) that attempts to find if a number is not prime using the [Lenstra elliptic-curve factorization](https://en.wikipedia.org/wiki/Lenstra_elliptic-curve_factorization) algorithm.
Using Lenstra helps this program purpose: determining if a number is not prime by finding small factors in large composite numbers.

## Usage
Run the program with the required arguments:

```bash
python lenstra.py -n <number> [-i <iterations>] [-v] [-b <base>]
```

### Arguments

| Argument | Optional                | Description                                                                      |
|:--------:|:-----------------------:|----------------------------------------------------------------------------------|
| `-n`     | :x:                     | The number to test                                                               |
| `-i`     | :white_check_mark:      | The maximum number of iterations for the algorithm                               |
| `-b`     | :white_check_mark:      | Base of the number to test (binary=bin, octal=oct, decimal=dec, hexadecimal=hex) |
| `-v`     | :white_check_mark:      | Enables extra logging for debugging and detailed output                          |

### Example

The following execution will attempt to find factors of 5615377489327409283 (4DEDD4133315C883 in hexadecimal) 
using up to 200 iterations with verbose logging enabled. Note that you can also write the hexadecimal 
digits in lowercase.

```
# python lenstra.py -n 0x4DEDD4133315C883 -i 200 -v -b hex
Iteration 0. Using curve y^2 = x^3 + ax + b where
a = 0x32ff02ef747aab6c
b = 0x207d0af3
And initial point = (0x0, 0x41f7fd071c5e2a9)

End of procedure: 0x4dedd4133315c883 is not prime.
```
> [!IMPORTANT]  
> The Lenstra algorithm is probabilistic and may not always find factors within the given iteration limit.
> For large numbers, increasing the iteration count may improve the chance of finding factors.

You can take a look to this [standard curve database](https://neuromancer.sk/std/) and check the parameter `n`
that are always prime numbers. For example, the result for `n` in the curve [P-384](https://neuromancer.sk/std/nist/P-384)
is the following, telling the user that the number is prime or the generated curves are not ideal:

```
# python lenstra.py -n 0x2f40e7e2221f295de297117b7f3d62f5c6a97ffcb8ceff1cd6ba8ce4a9a18ad84ffabbd8efa59332be7ad6756a66e294afd185a78ff12aa520e4de739baca0c7ffeff7f2955727a -i 200 -v -b hex

Iteration 0. Using curve y^2 = x^3 + ax + b where
a = 0x15ac38993d6ec26cd4fb822431d55579018b1e66ee161d22cbe1e7bc97aecbf30c216c1e62a5491a20515bc15d50e4cd47706602c2396e043c4c99c2653a1501fb78d072b04efbe
b = 0x13672480fc341c9fc25ce483c3184e7b7c4df03b826ef558f15072ef96c19d8c82e43931
And initial point = (0x0, 0x17878f98a6f361a9408620e18e759aefcc3859bc560deda983124f4e7645228bf64fb79234576b23aeac76db7e3f7b6851b19539974cc14095b660141e8e24d02933d23b00edb61)
...

Iteration 199. Using curve y^2 = x^3 + ax + b where
a = 0x11c66eb9841dcc60d0cf5d15278b7fe54ed78cb0fd2c8e91562701868a68dd56f5ed580221734837d46337608fa86576960968e0635de019c215fd55d1e87fb2d409d3efab7dde9
b = 0x15fe529f56c633d7b1df33a111f40b364da437089c47731ad61074c1fa9a8717abe1a975
And initial point = (0x0, 0x1e3b63633172c942407ed8df88fbe41111cc4d3345eefcaeb99ae707a6569daff7cacc12ababf30bf2c515747f70438007cfaefd6abfb82920d9fdf81ed0e5abb7118539dd5af79)

End of procedure. Maybe 0x3ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe661ce18ff55987308059b186823851ec7dd9ca1161de93d5174d66e8382e9bb2fe84e47 is prime or the generated curves are not ideal.
```

## References

- [Corbellini, A. (2015, May 17). *Elliptic Curve Cryptography: A Gentle Introduction*](https://andrea.corbellini.name/2015/05/17/elliptic-curve-cryptography-a-gentle-introduction/)
- [RareSkills. (2024, August 26). *Group Theory*](https://www.rareskills.io/post/group-theory)
- [RareSkills. (2023, September 26). *Elliptic Curve Addition*](https://www.rareskills.io/post/elliptic-curve-addition)
- [Dattoli, G., Sabia, E., & Tata, A. (2024). *Mathematics*, 12(6), 881](https://www.mdpi.com/2227-7390/12/6/881)
