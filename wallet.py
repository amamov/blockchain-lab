from typing import cast
from ecdsa import NIST256p
from ecdsa import SigningKey, VerifyingKey


class Wallet:
    def __init__(self):
        self.__private_key = SigningKey.generate(curve=NIST256p)
        self.__public_key = cast(VerifyingKey, self.__private_key.get_verifying_key())

    @property
    def private_key(self):
        return self.__private_key.to_string().hex()

    @property
    def public_key(self):
        print(type(self.__public_key))
        return self.__public_key.to_string().hex()


"""
1. creating a public ket with ECDSA
2. SHA-256 for the public key
3. Ripemd160 for the SHA-256
4. Add network byte
5. Double SHA-256
6. Get checksum
7. Concatenate public key and checksum
8. Encoding the key with Base58
"""


if __name__ == "__main__":
    wallet = Wallet()
    print(type(wallet.public_key))
