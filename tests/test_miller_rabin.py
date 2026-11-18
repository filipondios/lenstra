from lib.miller_rabin import is_prime


def test_edge_cases():
    assert not is_prime(0)
    assert not is_prime(1)
    assert is_prime(2)
    assert is_prime(3)
    for power in (4, 8, 16, 32, 64):
        assert not is_prime(power)
    assert not is_prime(9)


def test_carmichael():
    # Composites that fool Fermat's test for every coprime base.
    for n in (561, 1105, 1729):
        assert not is_prime(n)


def test_known_primes_and_pseudoprimes():
    # 2^61 - 1 is a Mersenne prime; 3215031751 is a strong pseudoprime in bases 2,3,5,7,11.
    assert is_prime(2**61 - 1)
    assert not is_prime(3215031751)


def test_n_above_2_64():
    # Outside the deterministic range: 40 random bases.
    assert is_prime(2**127 - 1, 40)
    assert not is_prime((2**61 - 1) * (2**31 - 1), 40)
