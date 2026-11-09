"""A small educational AES-128 implementation.

Only encryption is implemented here because the CTR mode example only needs
AES encryption. This is intentionally not a complete AES API.
"""

SBOX = (
0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16)

RCON = (0, 1, 2, 4, 8, 16, 32, 64, 128, 27, 54)


def _xtime(value: int) -> int:
    """Multiply a GF(2^8) value by x."""
    value <<= 1
    if value & 0x100:
        value ^= 0x11B
    return value & 0xFF


def gf_mul(a: int, b: int) -> int:
    """Multiply two bytes in GF(2^8)."""
    result = 0
    left = a & 0xFF
    right = b & 0xFF

    for _ in range(8):
        if right & 1:
            result ^= left
        left = _xtime(left)
        right >>= 1

    return result & 0xFF


def _add_round_key(state, round_key):
    return [x ^ y for x, y in zip(state, round_key)]


def _sub_bytes(state):
    return [SBOX[x] for x in state]


def _shift_rows(state):
    # AES stores the state column by column in this implementation.
    shifted = [0] * 16
    for row in range(4):
        for column in range(4):
            source_column = (column + row) % 4
            shifted[4 * column + row] = state[4 * source_column + row]
    return shifted


def _mix_columns(state):
    mixed = [0] * 16

    for column in range(4):
        i = column * 4
        a0, a1, a2, a3 = state[i:i + 4]

        mixed[i] = gf_mul(a0, 2) ^ gf_mul(a1, 3) ^ a2 ^ a3
        mixed[i + 1] = a0 ^ gf_mul(a1, 2) ^ gf_mul(a2, 3) ^ a3
        mixed[i + 2] = a0 ^ a1 ^ gf_mul(a2, 2) ^ gf_mul(a3, 3)
        mixed[i + 3] = gf_mul(a0, 3) ^ a1 ^ a2 ^ gf_mul(a3, 2)

    return mixed


def _expand_key(key: bytes):
    if len(key) != 16:
        raise ValueError("AES-128 needs a 16-byte key")

    # Four words make the original 128-bit key.
    words = [list(key[i:i + 4]) for i in range(0, 16, 4)]

    while len(words) < 44:
        word = words[-1][:]
        word_index = len(words)

        if word_index % 4 == 0:
            word = word[1:] + word[:1]
            word = [SBOX[value] for value in word]
            word[0] ^= RCON[word_index // 4]

        previous = words[-4]
        new_word = [previous[i] ^ word[i] for i in range(4)]
        words.append(new_word)

    round_keys = []
    for round_number in range(11):
        start = round_number * 4
        round_keys.append(sum(words[start:start + 4], []))

    return round_keys


class AES128:
    """AES-128 encryption for learning and testing."""

    def __init__(self, key: bytes):
        self.round_keys = _expand_key(key)

    def encrypt_block(self, block: bytes) -> bytes:
        """Encrypt one 16-byte block."""
        if len(block) != 16:
            raise ValueError("AES blocks are exactly 16 bytes")

        state = list(block)
        state = _add_round_key(state, self.round_keys[0])

        for round_number in range(1, 10):
            state = _sub_bytes(state)
            state = _shift_rows(state)
            state = _mix_columns(state)
            state = _add_round_key(state, self.round_keys[round_number])

        # The last AES round does not use MixColumns.
        state = _sub_bytes(state)
        state = _shift_rows(state)
        state = _add_round_key(state, self.round_keys[10])

        return bytes(state)


def aes128_ctr(key: bytes, nonce: bytes, data: bytes) -> bytes:
    """Encrypt/decrypt data using AES-128 in a simple CTR construction.

    The nonce is 8 bytes and the counter is another 8 bytes. Reusing the same
    nonce with the same key for different plaintexts is unsafe in CTR mode.
    """
    if len(key) != 16:
        raise ValueError("AES-128 needs a 16-byte key")
    if len(nonce) != 8:
        raise ValueError("nonce must be exactly 8 bytes")

    cipher = AES128(key)
    output = bytearray()

    for counter, start in enumerate(range(0, len(data), 16)):
        counter_bytes = counter.to_bytes(8, "big")
        keystream = cipher.encrypt_block(nonce + counter_bytes)
        block = data[start:start + 16]

        for plain_byte, stream_byte in zip(block, keystream):
            output.append(plain_byte ^ stream_byte)

    return bytes(output)
