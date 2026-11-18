from math import prod
from random import sample, seed

import pytest

from lib.factor import FactorizationIncomplete, _ecm, factorize
from lib.miller_rabin import is_prime


def test_basic_cases():
    assert factorize(1) == {}
    assert factorize(2) == {2: 1}
    assert factorize(104729) == {104729: 1}
    assert factorize(9) == {3: 2}
    assert factorize(12) == {2: 2, 3: 1}
    assert factorize(16) == {2: 4}
    assert factorize(49) == {7: 2}
    assert factorize(561) == {3: 1, 11: 1, 17: 1}


def test_pseudoprime_and_semiprime():
    # Carmichael number with factors 151, 751, 28351; semiprime with ~40-bit factors.
    assert factorize(3215031751) == {151: 1, 751: 1, 28351: 1}
    assert factorize(1000003 * 1000033) == {1000003: 1, 1000033: 1}
    # ~64-bit semiprime with two 32-bit primes.
    assert factorize(4294967291 * 4294967279) == {4294967279: 1, 4294967291: 1}


def test_invariant_for_small_numbers():
    for n in range(2, 2000):
        factors = factorize(n)
        assert prod(p ** e for p, e in factors.items()) == n
        assert all(is_prime(p) for p in factors)


def test_property_200_random_numbers():
    seed(1234)
    for n in sample(range(2, 10**9), 200):
        factors = factorize(n)
        assert prod(p ** e for p, e in factors.items()) == n
        assert all(is_prime(p) for p in factors)


def test_ecm_finds_divisor():
    seed(0)
    d = _ecm(15, b1=10, curves=100, verbose=False)
    assert d in (3, 5)


def test_incomplete_factorization():
    n = (2**61 - 1) * (2**31 - 1)
    with pytest.raises(FactorizationIncomplete):
        factorize(n, b1=2, curves=1)
