"""A few byte helpers used by the examples and tests."""


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR two byte strings of the same length."""
    if len(a) != len(b):
        raise ValueError("xor_bytes needs inputs with the same length")

    result = bytearray(len(a))
    for i in range(len(a)):
        result[i] = a[i] ^ b[i]
    return bytes(result)


def chunks(data: bytes, size: int):
    """Yield `data` in pieces of at most `size` bytes."""
    if size <= 0:
        raise ValueError("size must be positive")

    position = 0
    while position < len(data):
        yield data[position:position + size]
        position += size
