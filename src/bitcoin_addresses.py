import hashlib

from base58 import b58encode_check
from ecdsa import VerifyingKey

from src.adapters import get_confirmed_sat_balance


class P2PKH:
    def __init__(self, pem):
        self.public_key = pem
        self.confirmed_balance = get_confirmed_sat_balance(self.address)

    @property
    def btc_public_key(self):
        vk = VerifyingKey.from_pem(self.public_key)
        btc_public_key = bytes.fromhex('04') + vk.to_string()

        return btc_public_key.hex()

    @property
    def address(self):
        sha256 = hashlib.sha256(bytes.fromhex(self.btc_public_key)).digest()

        ripemd160_hash = hashlib.new('ripemd160')
        ripemd160_hash.update(sha256)
        ripemd160 = ripemd160_hash.digest()

        hashed_btc_public_key = bytes.fromhex('00') + ripemd160

        addr = b58encode_check(hashed_btc_public_key).decode('utf-8')

        return addr
