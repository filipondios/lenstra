from random import randrange

# Bases que hacen el test determinista para todo n < 2^64.
BASES_64 = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


def is_prime(n: int, rounds: int = 40) -> bool:
    """Miller-Rabin test: always false for a composite, true with high probability."""
    if n < 2:
        return False

    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p

    d, s = n - 1, 0
    while d % 2 == 0:
        s += 1
        d //= 2

    # shortcut: para n >= 2^64 es probabilístico; subir `rounds` reduce el error a 4^-rounds.
    bases = BASES_64 if n < 1 << 64 else (randrange(2, n - 1) for _ in range(rounds))

    for a in bases:
        a %= n
        if a == 0:
            continue

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else: return False
    return True
