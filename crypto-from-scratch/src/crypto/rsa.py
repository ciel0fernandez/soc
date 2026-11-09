"""Educational textbook RSA operations."""

from dataclasses import dataclass

from .number_theory import gcd, mod_inverse, mod_pow, random_prime
from .sha256 import sha256


@dataclass(frozen=True)
class RSAKeyPair:
    """The public and private values for the small demo implementation."""

    n: int
    e: int
    d: int

    @property
    def public_key(self):
        return self.n, self.e

    @property
    def private_key(self):
        return self.n, self.d

    @property
    def bits(self) -> int:
        return self.n.bit_length()


def generate_keypair(bits: int = 1024) -> RSAKeyPair:
    """Generate an educational RSA key pair."""
    if bits < 512:
        raise ValueError("use at least 512 bits for this demo")

    half = bits // 2
    p = random_prime(half)
    q = random_prime(half)

    while p == q:
        q = random_prime(half)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537

    # It is extremely unlikely for this to happen with normal RSA primes,
    # but checking it makes the assumption explicit.
    while gcd(e, phi) != 1:
        p = random_prime(half)
        q = random_prime(half)
        while p == q:
            q = random_prime(half)
        n = p * q
        phi = (p - 1) * (q - 1)

    d = mod_inverse(e, phi)
    return RSAKeyPair(n=n, e=e, d=d)


def _bytes_to_int(message: bytes) -> int:
    return int.from_bytes(message, "big")


def _int_to_bytes(value: int, length=None) -> bytes:
    if length is None:
        length = max(1, (value.bit_length() + 7) // 8)
    return value.to_bytes(length, "big")


def rsa_encrypt(message: bytes, public_key) -> int:
    """Encrypt a small message using textbook RSA."""
    n, e = public_key
    message_int = _bytes_to_int(message)

    if message_int >= n:
        raise ValueError("message is too large for this RSA modulus")

    return mod_pow(message_int, e, n)


def rsa_decrypt(ciphertext: int, private_key, length=None) -> bytes:
    """Decrypt a textbook RSA ciphertext."""
    n, d = private_key
    if not 0 <= ciphertext < n:
        raise ValueError("ciphertext is outside the RSA modulus")

    message_int = mod_pow(ciphertext, d, n)
    return _int_to_bytes(message_int, length)


def sign_message(message: bytes, private_key) -> int:
    """Make the simple textbook-RSA signature used by the demo.

    This is intentionally NOT RSA-PSS and must not be used as a real
    signature format.
    """
    n, d = private_key
    digest = _bytes_to_int(sha256(message))

    if digest >= n:
        raise ValueError("SHA-256 digest is too large for this RSA key")

    return mod_pow(digest, d, n)


def verify_message(message: bytes, signature: int, public_key) -> bool:
    """Check the demo signature against a message."""
    n, e = public_key
    if not 0 <= signature < n:
        return False

    expected = _bytes_to_int(sha256(message))
    actual = mod_pow(signature, e, n)
    return actual == expected
