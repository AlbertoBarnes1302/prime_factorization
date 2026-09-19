"""Tests for prime_factorization.core."""

import unittest

from prime_factorization import factorize, is_prime, prime_factors


class TestIsPrime(unittest.TestCase):
    def test_small_primes(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
        for p in primes:
            self.assertTrue(is_prime(p), f"{p} should be prime")

    def test_small_composites(self):
        composites = [0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 21, 25, 27, 35, 49]
        for n in composites:
            self.assertFalse(is_prime(n), f"{n} should not be prime")

    def test_large_prime(self):
        # 2**61 - 1 is a Mersenne prime, well within our range.
        self.assertTrue(is_prime(2**61 - 1))

    def test_large_composite(self):
        # Product of two large primes.
        self.assertFalse(is_prime(1000000007 * 1000000009))


class TestPrimeFactors(unittest.TestCase):
    def test_one(self):
        self.assertEqual(prime_factors(1), [])

    def test_zero_raises(self):
        with self.assertRaises(ValueError):
            prime_factors(0)

    def test_negative_raises(self):
        with self.assertRaises(ValueError):
            prime_factors(-5)

    def test_prime_input(self):
        self.assertEqual(prime_factors(13), [13])

    def test_composite_small(self):
        self.assertEqual(prime_factors(12), [2, 2, 3])

    def test_composite_large(self):
        n = 2**10 * 3**5 * 5**2 * 7
        self.assertEqual(prime_factors(n), [2]*10 + [3]*5 + [5]*2 + [7])

    def test_perfect_power(self):
        self.assertEqual(prime_factors(2**20), [2]*20)

    def test_semiprime(self):
        p = 1000000007
        q = 1000000009
        n = p * q
        self.assertEqual(prime_factors(n), [p, q])


class TestFactorize(unittest.TestCase):
    def test_one(self):
        self.assertEqual(factorize(1), {})

    def test_prime(self):
        self.assertEqual(factorize(17), {17: 1})

    def test_composite(self):
        self.assertEqual(factorize(12), {2: 2, 3: 1})

    def test_large_composite(self):
        n = 2**5 * 3**3 * 5
        self.assertEqual(factorize(n), {2: 5, 3: 3, 5: 1})


if __name__ == "__main__":
    unittest.main()
