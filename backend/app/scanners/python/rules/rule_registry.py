from app.scanners.python.rules.md5_rule import MD5Rule
from app.scanners.python.rules.sha1_rule import SHA1Rule
from app.scanners.python.rules.sha224_rule import SHA224Rule
from app.scanners.python.rules.sha256_rule import SHA256Rule
from app.scanners.python.rules.sha384_rule import SHA384Rule
from app.scanners.python.rules.sha512_rule import SHA512Rule
from app.scanners.python.rules.aes_rule import AESRule
from app.scanners.python.rules.des_rule import DESRule
from app.scanners.python.rules.triple_des_rule import TripleDESRule
from app.scanners.python.rules.rc4_rule import RC4Rule
from app.scanners.python.rules.chacha20_rule import ChaCha20Rule
from app.scanners.python.rules.rsa_rule import RSARule
from app.scanners.python.rules.ecc_rule import ECCRule
from app.scanners.python.rules.ecdsa_rule import (
    ECDSARule,
)
from app.scanners.python.rules.ecdh_rule import (
    ECDHRule,
)
class RuleRegistry:

    @staticmethod
    def get_rules():

        return [
            MD5Rule(),
            SHA1Rule(),
            SHA224Rule(),
            SHA256Rule(),
            SHA384Rule(),
            SHA512Rule(),

            AESRule(),
            DESRule(),
            TripleDESRule(),
            RC4Rule(),
            ChaCha20Rule(),
            # existing hash rules
            # existing symmetric rules
            RSARule(),
            ECCRule(),
            ECDSARule(),
            ECDHRule(),
        ]