# A bit of the math behind the project

This file is not meant to be a full cryptography textbook. It is just a place to keep the math ideas that show up in the code.

## AES and GF(2^8)

AES works with bytes, but the operations inside AES are not ordinary integer arithmetic everywhere. A byte can be treated as an element of the finite field GF(2^8).

The implementation uses that idea in `gf_mul()` for the MixColumns step.

The main AES-128 steps are:

1. AddRoundKey
2. SubBytes
3. ShiftRows
4. MixColumns
5. AddRoundKey again

There are 10 rounds for AES-128. The last round skips MixColumns.

The S-box is a fixed lookup table. The key expansion turns the original 16-byte key into the round keys used by all 10 rounds.

## RSA

RSA starts with two prime numbers, usually called `p` and `q`.

```text
n = p * q
phi(n) = (p - 1) * (q - 1)
```

Then we choose a public exponent `e` and find `d` such that:

```text
e * d = 1 (mod phi(n))
```

Encryption in this educational implementation is the textbook operation:

```text
c = m^e mod n
```

and decryption is:

```text
m = c^d mod n
```

The code uses fast modular exponentiation instead of calculating huge powers directly.

Prime generation uses Miller-Rabin as a probable-prime test. That does not mean the generated number is mathematically proven prime by this function; it means it passes the selected probabilistic tests.

## SHA-256

SHA-256 is a hash function, not an encryption algorithm. You cannot normally take a SHA-256 digest and decrypt it back into the original message.

The implementation does roughly this:

1. Add the SHA-256 padding.
2. Split the message into 512-bit blocks.
3. Turn each block into a 64-word message schedule.
4. Run 64 compression rounds.
5. Add the result back into the eight working hash values.
6. Join those values into the final 256-bit digest.

A lot of the code is just careful 32-bit arithmetic, rotations and bitwise operations.

## PKCS#7

PKCS#7 padding makes a byte string fit an exact block size. If a message needs three padding bytes, each of those bytes has the value `03`.

The unpadding code checks that all padding bytes have the expected value before removing them.

## Security notes

The implementations here are intentionally educational.

- Textbook RSA is not safe for real encryption.
- The RSA signature example is not RSA-PSS.
- AES-CTR gives confidentiality but does not authenticate the data.
- Nonces/counters have to be managed correctly.
- Real cryptographic implementations also have to care about side channels, key storage, randomness, error handling and protocol design.

So the interesting part of this repo is the algorithms and the math, not using these functions as a replacement for a real crypto library.
