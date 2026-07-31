from app.scanners.python.rules.md5_rule import MD5Rule
from app.scanners.python.rules.sha1_rule import SHA1Rule

class RuleRegistry:

    @staticmethod
    def get_rules():

        return [
            MD5Rule(),
            SHA1Rule(),
        ]