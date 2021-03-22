# Standard
import os
import tempfile
import logging
from hashlib import sha256
from random import shuffle
from pathlib import Path, PurePath
from typing import Dict, List, Generator

# Third Party
from diskcache import FanoutCache

LOG = logging.getLogger(__name__)


def get_cache_path(value: str) -> PurePath:
    """From a given seed value determine the cache folder."""
    try:
        cache_parent = Path.home()
    except AttributeError:
        try:
            cache_parent = Path(os.path.expanduser("~"))  # Older Py3 Fallback
        except Exception:
            cache_parent = Path(tempfile.gettempdir())
    return cache_parent.joinpath(".maagnar", hash_str(value))


def get_cache(value: str) -> FanoutCache:
    return FanoutCache(
        get_cache_path(value),
        size_limit=int(1e12),  # 1000 GB
        cull_limit=0,
        shards=8,
        sqlite_mmap_size=256,
    )


def shuffle_str(value: str) -> str:
    chars: List[str] = list(value)  # Convert to array of chars
    shuffle(chars)
    return "".join(chars)


def factorial(value: int) -> int:
    LOG.debug("Calculating factorial value for #c<%s>", value)
    # Check if the number is negative, positive or zero
    if value < 0:
        raise ValueError("Value cannot be negative")
    elif value == 0:
        return 1
    else:
        f = 1  # Starting value
        for i in range(1, value + 1):
            f = f * i
        return f


def calculate_total_permutations(value: str) -> int:
    """Calulate how many possible permutations are possible for a string."""
    # The simple path: when there are no repeated letters in a given string,
    # the total possible permutations is simply the factorial of the total
    # letter count.
    if len(value) == len(set(value)):
        return factorial(len(value))

    count_map: Dict[str, int] = {}
    for char in value:
        if char in count_map:
            count_map[char] += 1
        else:
            count_map[char] = 1

    base_factor = factorial(len(value))
    additional_factors = [factorial(x) for x in count_map.values()]
    result = 1
    for x in additional_factors:
        result = result * x
    return int(base_factor / result)


def permutations(value: str, clear_cache: bool = True) -> Generator[str, None, None]:
    """
    Yield anagrams of a given string.

    This is a generator; in some cases it'll be slower than just calculating
    all possible anagrams but it's good enough. On the first iteration, always
    return the initial value.

    If clear_cache is set to False, the tool will remember any anagrams it has
    already generated.
    """
    cache = get_cache(value)
    if clear_cache is True:
        cache.clear()

    cache.add(hash_str(value), 1)
    possible = calculate_total_permutations(value)
    if len(cache) >= possible:
        return  # The permutations are fully exhausted already

    yield value
    while True:
        if len(cache) >= possible:
            break
        anagram = shuffle_str(value)
        while True:
            new = cache.add(hash_str(anagram), 1)
            if new is True:
                break
            else:
                anagram = shuffle_str(anagram)
        yield anagram


def hash_str(value: str) -> str:
    """
    Generate a consistant hash value for a given string.

    The __hash__ magic methods are randomized between runs in Python3.x This
    provides a hash of a given value that is consisten between invocations of
    the Python interpreter.
    """
    hasher = sha256()
    hasher.update("maagnar-salt".encode("utf-8"))
    hasher.update(value.encode("utf-8"))
    return hasher.hexdigest()
