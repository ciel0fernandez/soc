"""Small RSA demo. The key size is intentionally small because this is a demo."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from crypto.rsa import (
    generate_keypair,
    rsa_decrypt,
    rsa_encrypt,
    sign_message,
    verify_message,
)


key = generate_keypair(512)
message = b"Hello RSA!"

ciphertext = rsa_encrypt(message, key.public_key)
recovered = rsa_decrypt(ciphertext, key.private_key, len(message))

signature = sign_message(message, key.private_key)
valid = verify_message(message, signature, key.public_key)

print("Key bits:", key.bits)
print("Ciphertext:", ciphertext)
print("Recovered:", recovered)
print("Signature valid:", valid)
print("Wrong message valid:", verify_message(b"not the same", signature, key.public_key))
