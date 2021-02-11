# Standard
import logging
from random import shuffle
from typing import Dict, List, Generator

LOG = logging.getLogger(__name__)


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


def permutations(value: str) -> Generator[str, None, None]:
    """
    Yield anagrams of a given string.

    This is a generator; in some cases it'll be slower than just calculating
    all possible anagrams but it's good enough. On the first iteration, always
    return the initial value.
    """
    seen = {value}
    possible = calculate_total_permutations(value)
    yield value
    while True:
        if len(seen) >= possible:
            break
        anagram = shuffle_str(value)
        while True:
            if anagram not in seen:
                seen.add(anagram)
                break
            anagram = shuffle_str(anagram)
        yield anagram
