"""Small AES-CTR demo."""

import sys
from pathlib import Path

# This keeps the example runnable without installing the package first.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from crypto.aes import aes128_ctr


key = b"0123456789abcdef"
nonce = b"12345678"
message = b"Cryptography from scratch!"

ciphertext = aes128_ctr(key, nonce, message)
recovered = aes128_ctr(key, nonce, ciphertext)

print("Plaintext :", message)
print("Ciphertext:", ciphertext.hex())
print("Recovered :", recovered)
print("Round trip:", recovered == message)
