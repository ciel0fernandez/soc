import hashlib

from crypto.sha256 import sha256


def test_sha256_known_messages():
    messages = (
        b"",
        b"hello",
        b"abc" * 1000,
        bytes(range(256)),
    )

    for data in messages:
        assert sha256(data) == hashlib.sha256(data).digest()


def test_sha256_hex_output_matches_standard_library():
    data = b"learning how hashes work"
    assert sha256(data).hex() == hashlib.sha256(data).hexdigest()
