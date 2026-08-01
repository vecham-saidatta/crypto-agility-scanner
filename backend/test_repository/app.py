import hashlib
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from hashlib import md5, sha256
from cryptography.hazmat.primitives import hashes

data = b"crypto agility"
md5_hash = hashlib.md5(data).hexdigest()
sha1_hash = hashlib.sha1(data).hexdigest()
sha224_hash = hashlib.sha224(data).hexdigest()
sha256_hash = hashlib.sha256(data).hexdigest()
sha384_hash = hashlib.sha384(data).hexdigest()
sha512_hash = hashlib.sha512(data).hexdigest()

key = b"0" * 32

aes = algorithms.AES(key)
triple_des = algorithms.TripleDES(b"0" * 24)
arc4 = algorithms.ARC4(b"0" * 16)
chacha = algorithms.ChaCha20(key, b"0" * 16)

data2 = b"direct import test"

direct_md5 = md5(data2)
direct_sha256 = sha256(data2)

direct_aes = AES(b"0" * 32)

def md5(data):
    return data


fake_md5 = md5(b"not cryptography")

class FakeCrypto:

    @staticmethod
    def md5(data):
        return data


fake_crypto = FakeCrypto()

fake_result = fake_crypto.md5(
    b"this is not hashlib"
)

from cryptography.hazmat.primitives.asymmetric import rsa


rsa_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

from cryptography.hazmat.primitives.asymmetric import ec


ecc_private_key = ec.generate_private_key(
    ec.SECP256R1()
)

ecdsa_algorithm = ec.ECDSA(
    hashes.SHA256()
)