import ast

from app.scanners.python.import_resolver import ImportResolver


def test_resolves_direct_hashlib_import():

    source = """
from hashlib import md5
"""

    tree = ast.parse(source)

    resolver = ImportResolver()

    symbols = resolver.resolve(tree)

    assert "md5" in symbols

    assert symbols["md5"] == [
        (2, "hashlib.md5")
    ]


def test_resolves_import_alias():

    source = """
import hashlib as hl
"""

    tree = ast.parse(source)

    resolver = ImportResolver()

    symbols = resolver.resolve(tree)

    assert "hl" in symbols

    assert symbols["hl"] == [
        (2, "hashlib")
    ]


def test_tracks_function_shadowing():

    source = """
from hashlib import md5

real_hash = md5(b"hello")

def md5(data):
    return data

fake_hash = md5(b"hello")
"""

    tree = ast.parse(source)

    resolver = ImportResolver()

    symbols = resolver.resolve(tree)

    assert symbols["md5"] == [
        (2, "hashlib.md5"),
        (6, None),
    ]