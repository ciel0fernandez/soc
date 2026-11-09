"""Small educational cryptography implementations.

Nothing in this package should be treated as production crypto code.
"""

from .aes import AES128, aes128_ctr
from .number_theory import (
    gcd,
    extended_gcd,
    mod_inverse,
    mod_pow,
    is_probable_prime,
    random_prime,
)
from .padding import pkcs7_pad, pkcs7_unpad
from .rsa import RSAKeyPair, generate_keypair, rsa_encrypt, rsa_decrypt
from .sha256 import sha256

__all__ = [
    "AES128",
    "aes128_ctr",
    "gcd",
    "extended_gcd",
    "mod_inverse",
    "mod_pow",
    "is_probable_prime",
    "random_prime",
    "pkcs7_pad",
    "pkcs7_unpad",
    "RSAKeyPair",
    "generate_keypair",
    "rsa_encrypt",
    "rsa_decrypt",
    "sha256",
]
