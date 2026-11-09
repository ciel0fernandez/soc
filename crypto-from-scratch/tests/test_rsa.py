from crypto.number_theory import gcd, mod_inverse, mod_pow
from crypto.rsa import generate_keypair, rsa_decrypt, rsa_encrypt, sign_message, verify_message


def test_number_theory_basics():
    assert gcd(48, 18) == 6
    assert mod_inverse(3, 11) == 4
    assert mod_pow(2, 10, 1000) == 24


def test_rsa_round_trip():
    key = generate_keypair(512)
    message = b"hello RSA"

    ciphertext = rsa_encrypt(message, key.public_key)
    assert rsa_decrypt(ciphertext, key.private_key, len(message)) == message


def test_rsa_rejects_too_large_message():
    key = generate_keypair(512)
    too_large = key.n.to_bytes((key.n.bit_length() + 7) // 8, "big")

    try:
        rsa_encrypt(too_large, key.public_key)
    except ValueError:
        pass
    else:
        raise AssertionError("an integer >= n should be rejected")


def test_signature():
    key = generate_keypair(512)
    message = b"authenticated"
    signature = sign_message(message, key.private_key)

    assert verify_message(message, signature, key.public_key)
    assert not verify_message(b"tampered", signature, key.public_key)
