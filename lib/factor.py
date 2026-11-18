from math import gcd, lcm, prod
from lib.curve import Curve, InversionImpossible
from lib.miller_rabin import is_prime


class FactorizationIncomplete(Exception):
    """No method found a factor within the given limits."""


def factorize(n: int, b1: int = 10000, curves: int = 100, rounds: int = 40,
    verbose: bool = False) -> dict[int, int]:
    """Return {prime: exponent} for n >= 1."""
    factors = {}
    _factorize(n, b1, curves, rounds, verbose, factors)
    assert prod(p ** e for p, e in factors.items()) == n
    return dict(sorted(factors.items()))


def _factorize(n: int, b1: int, curves: int, rounds: int, verbose: bool,
    factors: dict[int, int]) -> None:
    if n == 1:
        return
    if is_prime(n, rounds):
        factors[n] = factors.get(n, 0) + 1
        return

    d = _find_factor(n, b1, curves, verbose)
    if d is None:
        raise FactorizationIncomplete(n)

    _factorize(d, b1, curves, rounds, verbose, factors)
    _factorize(n // d, b1, curves, rounds, verbose, factors)


def _find_factor(n: int, b1: int, curves: int, verbose: bool) -> int | None:
    # Any composite divisor found here is split further by the recursion.
    for p in range(2, min(n, 1001)):
        if n % p == 0:
            return p

    d = _pollard_rho(n)
    if d is not None:
        return d
    return _ecm(n, b1, curves, verbose)


def _pollard_rho(n: int) -> int | None:
    if n % 2 == 0:
        return 2

    for c in range(1, 11):
        x = y = 2
        d = 1
        for _ in range(10000):
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
            if d != 1:
                break
        if 1 < d < n:
            return d
    return None


def _ecm(n: int, b1: int, curves: int, verbose: bool) -> int | None:
    # LCM of 1..B1 is a multiple of all small group orders.
    k = lcm(*range(1, b1 + 1))

    for i in range(curves):
        curve = Curve(n)
        point = curve.generate_point()

        if verbose:
            print(f'Curve {i}. b1={b1}. Using {curve}initial point = {point}')

        try:
            curve.mul_point(point, k)
        except InversionImpossible as e:
            d = gcd(e.denominator, n)
            if 1 < d < n:
                return d
    return None
