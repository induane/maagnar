# Project
from maagnar import lib


def test_permutations():
    seen = set()
    expected = {
        "estt",
        "etst",
        "etts",
        "sett",
        "stet",
        "stte",
        "test",
        "tets",
        "tset",
        "tste",
        "ttes",
        "ttse",
    }
    for anagram in lib.permutations("test"):
        seen.add(anagram)
    assert seen == expected


def test_calculate_total_permutations():
    assert lib.calculate_total_permutations("abcd") == 24
    assert lib.calculate_total_permutations("abca") == 12


def test_hash_str():
    """Hashing values is consistent between Python interpeter runs."""
    test_values = (
        ("test1", "fef6d48ce5bba44db91557f3902e3eadaa00ea0566979dc5afa53ba405feb275"),
        ("a sentence", "42e8b30a427a2952f6ce4c8aa992b981d017be09bb1f2874f103d10612777707"),
        ("Here have a cigar you're gonna go far", "1f8d4ad81539ffaa9b98abe0a31f01681539ca5edc29ea7be33cb43d13b5d43a"),
    )
    for input_val, output_val in test_values:
        assert lib.hash_str(input_val) == output_val
