"""Number theory helpers used by the educational RSA implementation."""

import secrets


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of two integers."""
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int):
    """Return (g, x, y) where a*x + b*y = g = gcd(a, b)."""
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y

    if old_r < 0:
        return -old_r, -old_x, -old_y
    return old_r, old_x, old_y


def mod_inverse(a: int, m: int) -> int:
    """Find x where (a*x) % m == 1, if it exists."""
    if m <= 0:
        raise ValueError("modulus must be positive")

    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("modular inverse does not exist")
    return x % m


def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """Fast modular exponentiation using repeated squaring."""
    if modulus <= 0:
        raise ValueError("modulus must be positive")
    if exponent < 0:
        raise ValueError("exponent must not be negative")

    result = 1 % modulus
    base %= modulus

    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1

    return result


def _decompose_even_part(number: int):
    """Write number as odd_part * 2**s."""
    s = 0
    odd_part = number
    while odd_part % 2 == 0:
        odd_part //= 2
        s += 1
    return odd_part, s


def is_probable_prime(n: int, rounds: int = 16) -> bool:
    """Run a Miller-Rabin probable-prime test."""
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if n in small_primes:
        return True
    if any(n % p == 0 for p in small_primes):
        return False
    if rounds <= 0:
        raise ValueError("rounds must be positive")

    d, s = _decompose_even_part(n - 1)

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = mod_pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        probably_ok = False
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                probably_ok = True
                break

        if not probably_ok:
            return False

    return True


def random_prime(bits: int) -> int:
    """Generate a probable prime with approximately `bits` bits."""
    if bits < 16:
        raise ValueError("use at least 16 bits")

    while True:
        candidate = secrets.randbits(bits)
        candidate |= 1 << (bits - 1)  # make sure the top bit is set
        candidate |= 1                 # and make it odd

        if is_probable_prime(candidate):
            return candidate
