"""PKCS#7 padding helpers."""


def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    """Pad a byte string to a multiple of block_size."""
    if not 1 <= block_size <= 255:
        raise ValueError("block_size must be between 1 and 255")

    padding_len = block_size - (len(data) % block_size)
    padding = bytes([padding_len]) * padding_len
    return data + padding


def pkcs7_unpad(data: bytes, block_size: int = 16) -> bytes:
    """Remove PKCS#7 padding and reject malformed padding."""
    if not 1 <= block_size <= 255:
        raise ValueError("block_size must be between 1 and 255")
    if not data or len(data) % block_size != 0:
        raise ValueError("invalid padded data")

    padding_len = data[-1]
    if padding_len == 0 or padding_len > block_size:
        raise ValueError("invalid PKCS#7 padding")

    expected = bytes([padding_len]) * padding_len
    if data[-padding_len:] != expected:
        raise ValueError("invalid PKCS#7 padding")

    return data[:-padding_len]
