# Prime Factorization

A small Python library for factoring integers up to around 10**18 using trial division, Pollard's rho, and deterministic Miller-Rabin primality testing. It has zero third-party dependencies.

## Usage

```python
from prime_factorization import factorize, is_prime, prime_factors

# Check primality
is_prime(1000000007)  # True

# Get prime factors as a list (with multiplicity)
prime_factors(12)  # [2, 2, 3]

# Get factorization as a dictionary {prime: exponent}
factorize(12)  # {2: 2, 3: 1}
```

## Why this library exists

Factoring integers is a common need in number theory and cryptography-adjacent code. Python's standard library does not provide a factorization function, and third-party packages like SymPy are heavy and may not be available in restricted environments. This library implements efficient algorithms that handle numbers up to about 10**18 quickly, without external dependencies.

## Edge cases

- `prime_factors` and `factorize` raise `ValueError` for negative numbers and zero. Factoring 0 is undefined, and negative integers are not supported by design.
- `prime_factors(1)` returns an empty list, and `factorize(1)` returns an empty dictionary.
- Pollard's rho is randomized; however, the implementation retries with different seeds and is practically deterministic in its output for the supported range.

## Exported names

- `is_prime(n: int) -> bool`
- `prime_factors(n: int) -> list[int]`
- `factorize(n: int) -> dict[int, int]`

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

