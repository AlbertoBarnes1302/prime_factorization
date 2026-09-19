"""Core factorization routines.

This module implements trial division, Miller-Rabin primality testing,
and Pollard's rho algorithm.  The target range is integers up to about
10**18, which is well within the capabilities of these algorithms while
keeping the code small and dependency-free.
"""

from __future__ import annotations

import math
import random
from collections.abc import Iterable
from typing import Dict, List, Optional, Tuple


def is_prime(n: int) -> bool:
    """Return True if n is a prime number.

    Uses a deterministic Miller-Rabin test for n < 3,317,044,064,679,887,385,961,981
    (approximately 3.3e24), which comfortably covers our target range up to 10**18.
    The bases used are known to be sufficient for this bound.
    """
    if n < 2:
        return False
    if n in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        return True
    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n % 7 == 0:
        return False

    # Write n - 1 = d * 2^s with d odd.
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Deterministic bases for n < 3.3e24.
    bases = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

    for a in bases:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _pollard_rho(n: int) -> int:
    """Return a non-trivial factor of composite n using Pollard's rho.

    This is a randomized algorithm; it uses Python's random module.
    The function may rarely fail to find a factor for a given seed,
    but it retries with different seeds.
    """
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3

    while True:
        c = random.randrange(1, n - 1)
        f = lambda x: (pow(x, 2, n) + c) % n
        x, y, d = 2, 2, 1

        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), n)

        if d != n:
            return d
        # If d == n, retry with a different c.


def _factor_recursive(n: int, factors: List[int]) -> None:
    """Recursively factor n and append prime factors to the list."""
    if n == 1:
        return
    if is_prime(n):
        factors.append(n)
        return

    # Trial division for small factors to speed up Pollard's rho.
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            while n % p == 0:
                factors.append(p)
                n //= p
            _factor_recursive(n, factors)
            return

    d = _pollard_rho(n)
    _factor_recursive(d, factors)
    _factor_recursive(n // d, factors)


def prime_factors(n: int) -> List[int]:
    """Return a sorted list of prime factors of n.

    Factors are repeated according to their multiplicity.  For example,
    prime_factors(12) returns [2, 2, 3].
    """
    if n < 0:
        raise ValueError("prime_factors() argument must be non-negative")
    if n == 0:
        raise ValueError("0 has no prime factorization")
    if n == 1:
        return []

    factors: List[int] = []
    _factor_recursive(n, factors)
    factors.sort()
    return factors


def factorize(n: int) -> Dict[int, int]:
    """Return the prime factorization of n as a dictionary.

    Keys are prime factors, values are their exponents.  For example,
    factorize(12) returns {2: 2, 3: 1}.
    """
    factors = prime_factors(n)
    result: Dict[int, int] = {}
    for p in factors:
        result[p] = result.get(p, 0) + 1
    return result
