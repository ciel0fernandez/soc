from crypto.aes import AES128, aes128_ctr, gf_mul
from crypto.padding import pkcs7_pad, pkcs7_unpad


def test_aes_known_vector():
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    plaintext = bytes.fromhex("00112233445566778899aabbccddeeff")
    expected = "69c4e0d86a7b0430d8cdb78070b4c55a"

    assert AES128(key).encrypt_block(plaintext).hex() == expected


def test_gf_multiplication_example():
    # Common AES finite-field example: 0x57 * 0x83 = 0xc1.
    assert gf_mul(0x57, 0x83) == 0xC1


def test_ctr_round_trip():
    key = b"0123456789abcdef"
    nonce = b"12345678"
    message = b"hello from crypto, this is a longer test too"

    ciphertext = aes128_ctr(key, nonce, message)
    assert ciphertext != message
    assert aes128_ctr(key, nonce, ciphertext) == message


def test_ctr_empty_message():
    assert aes128_ctr(b"0123456789abcdef", b"12345678", b"") == b""


def test_padding_full_block():
    data = b"a" * 16
    padded = pkcs7_pad(data, 16)
    assert len(padded) == 32
    assert pkcs7_unpad(padded, 16) == data


def test_padding_bad_value():
    try:
        pkcs7_unpad(b"abc\x04", 4)
    except ValueError:
        pass
    else:
        raise AssertionError("bad padding should fail")
