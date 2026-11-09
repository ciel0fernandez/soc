"""A small SHA-256 implementation for learning purposes."""

K = (
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2)

# SHA-256 uses eight fixed starting words and wraps additions to 32 bits.
H0 = (
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
)
MASK32 = 0xffffffff


def _right_rotate(value: int, amount: int) -> int:
    return ((value >> amount) | (value << (32 - amount))) & MASK32


def _pad(data: bytes) -> bytes:
    """Add the one-bit marker, zeros, and the original length."""
    bit_length = len(data) * 8
    message = data + b"\x80"
    message += b"\x00" * ((56 - len(message) % 64) % 64)
    message += bit_length.to_bytes(8, "big")
    return message


def _make_schedule(block: bytes):
    """Turn one 512-bit block into the 64 words used by the rounds."""
    words = [
        int.from_bytes(block[i:i + 4], "big")
        for i in range(0, 64, 4)
    ]

    for i in range(16, 64):
        x = words[i - 15]
        y = words[i - 2]

        sigma0 = _right_rotate(x, 7) ^ _right_rotate(x, 18) ^ (x >> 3)
        sigma1 = _right_rotate(y, 17) ^ _right_rotate(y, 19) ^ (y >> 10)

        words.append((words[i - 16] + sigma0 + words[i - 7] + sigma1) & MASK32)

    return words


def _compress(state, schedule):
    a, b, c, d, e, f, g, h = state

    for i in range(64):
        s1 = _right_rotate(e, 6) ^ _right_rotate(e, 11) ^ _right_rotate(e, 25)
        choose = (e & f) ^ ((~e) & g)
        temp1 = (h + s1 + choose + K[i] + schedule[i]) & MASK32

        s0 = _right_rotate(a, 2) ^ _right_rotate(a, 13) ^ _right_rotate(a, 22)
        majority = (a & b) ^ (a & c) ^ (b & c)
        temp2 = (s0 + majority) & MASK32

        # Keeping this as separate assignments makes the SHA-256 state update
        # a little easier to follow than one giant tuple assignment.
        h = g
        g = f
        f = e
        e = (d + temp1) & MASK32
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & MASK32

    return [
        (state[0] + a) & MASK32,
        (state[1] + b) & MASK32,
        (state[2] + c) & MASK32,
        (state[3] + d) & MASK32,
        (state[4] + e) & MASK32,
        (state[5] + f) & MASK32,
        (state[6] + g) & MASK32,
        (state[7] + h) & MASK32,
    ]


def sha256(data: bytes) -> bytes:
    """Calculate a SHA-256 digest without using hashlib internally."""
    if not isinstance(data, bytes):
        raise TypeError("sha256() expects bytes")

    message = _pad(data)
    state = list(H0)

    for offset in range(0, len(message), 64):
        block = message[offset:offset + 64]
        schedule = _make_schedule(block)
        state = _compress(state, schedule)

    return b"".join(value.to_bytes(4, "big") for value in state)
