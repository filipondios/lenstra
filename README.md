# Lenstra

A dependency-free integer factorization tool in Python. Given a number `n`, it
returns its prime factorization using [Miller–Rabin](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test), [trial division](https://en.wikipedia.org/wiki/Trial_division), [Pollard rho](https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm) and [elliptic-curve factorization](https://en.wikipedia.org/wiki/Lenstra_elliptic-curve_factorization) (ECM).

## Usage

```bash
python lenstra.py -n <number> [options]
```

| Option | Default | Description |
|:--|:--|:--|
| `-n`, `--number` | required | Number to factorize |
| `-b`, `--base` | `dec` | Input base: `bin`, `oct`, `dec`, `hex` (prefixes `0x`, `0b`, `0o` are accepted) |
| `-c`, `--curves` | `100` | Maximum number of ECM curves |
| `--b1` | `10000` | ECM smoothness bound: `k = lcm(1..B1)` |
| `--rounds` | `40` | Miller–Rabin rounds for `n >= 2^64` |
| `--seed` | random | Seed for the random generator, to reproduce a run |
| `-v`, `--verbose` | off | Print each ECM curve and the elapsed time |
| `--json` | off | Emit structured JSON output |

### Examples

```console
# testing a composite number
$ python lenstra.py -n 561
561 = 3 * 11 * 17  (composite, verified with Miller-Rabin)
```

```console
# testing a prime number
$ python lenstra.py -n 104729
104729 is prime (Miller-Rabin).
```

```console
# using hexadecimal format to test a composite number
$ python lenstra.py -n 0x4DEDD4133315C883 -b hex
0x4dedd4133315c883 = 0x3 * 0x3a86e5 * 0x719f36a66d  (composite, verified with Miller-Rabin)
```

```console
# using the json option for json structured output
$ python lenstra.py -n 1000036000099 --json
{"number": 1000036000099, "prime": false, "factors": {"1000003": 1, "1000033": 1}, "b1": 10000, "curves": 100, "seconds": 0.0009}
```

The base selected with `-b` also applies to the printed factors. In `--json`
output every number is decimal.

### Exit codes

| Code | Meaning |
|:--|:--|
| 0 | Factorization completed, or the number is prime |
| 1 | No complete factorization within `--b1`/`--curves`; the message suggests larger values |
| 2 | Invalid input (argparse) |

## How it works

Miller–Rabin does not factor: it is a primality test. The tool uses it as the
first filter, then tries three methods in this order:

1. **Miller–Rabin**: is `n` prime? If so, stop. For `n < 2^64` it uses 7 fixed
   bases and the result is deterministic. For `n >= 2^64` it uses `rounds` random
   bases (40 by default), so a "prime" answer is probabilistic: the error is at
   most `4^-rounds`. A "composite" answer is always certain, because a single
   failing base proves compositeness.
2. **Trial division**: divide by integers up to 1000.
3. **Pollard rho**: look for factors with `f(x) = x^2 + c`, trying `c = 1..10`.
4. **ECM (Lenstra)**: build curves `y^2 = x^3 + ax + b` modulo `n`, with a point
   that lies on the curve, and multiply it by `k = lcm(1..B1)`. When a modular
   inverse does not exist, the `gcd` reveals a factor.

Whenever a factor appears, the process repeats on that factor and on `n // factor`
until every piece is prime. Before returning, the tool checks that the product of
the factors, including their exponents, equals `n`.


## Development

```bash
uv run --with pytest pytest -q
```

GitHub Actions runs the same command on every push and pull request
([.github/workflows/tests.yml](.github/workflows/tests.yml)). The library is stored in [lib](lib/) and [lenstra.py](lenstra.py) is the
CLI.

## License

GPL-2.0. See [LICENSE](LICENSE).
