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
