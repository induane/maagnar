# Maagnar
<a href="https://pypi.python.org/pypi/maagnar"><img src="https://img.shields.io/pypi/v/maagnar.svg"></a>

A simple library and tool for generating anagrams. It is generally low memory
and feels reasonably fast.

The implementation here is mildly interesting. Rather than descend in a
predictable way through all possible anagrams in sequence using an anagram, the
generator simply keeps track of every anagram it's seen. Each iteration
randomly shuffles the text around. If it encounters a shuffle it's seen before,
it just tries again until a new one is found.

## Library
A few helpful utils are shipped in the ``lib`` module and available as top
level imports. ``permutations`` is the main utility; it is implemented as a
generator and yields a new anagram of the given string each iteration until all
possible anagrams are exhausted.

```
from maagnar import permutations


for anagram in permutations("sometext"):
    print(anagram)
```

You can also determine how many possible anagrams exist for a given string:

```
>>> from maagnar import calculate_total_permutations
>>> calculate_total_permutations("sometext")
10080
>>> calculate_total_permutations("abcd")
24
>>> calculate_total_permutations("abca")
12
```

## Command Line Utility
Installation includes an entry point called ``maagnar`` which can be use to
generate an anagrams list.

```
$ maagnar lol
INFO: Generating anagrams from lol
INFO: Possible combinations: 3
INFO: [1/3] Found: 'lol'
INFO: [2/3] Found: 'oll'
INFO: [3/3] Found: 'llo'
$
```

![example](https://raw.githubusercontent.com/induane/maagnar/main/example.jpg)

The entry point remembers previously seen anagrams. This isn't that interesting
when the number of possible anagrams is low, but for anagrams such as:

```
Just because some of us can read and write and do a little math, that doesn't mean we deserve to conquer the universe
```

The number possible permutations is extremely high. You might need to stop
after a few decades and let your computer rest for a while before returning to
the task in-progress.

To start an anagram generator over, use the ``--clear-seen`` switch:

```
$ maagnar lol --clear-seen
INFO: Generating anagrams from lol
INFO: Possible combinations: 3
INFO: [1/3] Found: 'lol'
INFO: [2/3] Found: 'llo'
INFO: [3/3] Found: 'oll'
$
```

## Installation
I'm on pypi!

```
$ pip install maagnar
```

## Features
- Simple to use
- Compatibility with Python 3.x, PyPy

## Makefile

This project uses a Makefile for various tasks. Some of the available tasks
are listed below.

* `make clean` - Clean build artifacts out of your project
* `make test` - Run Unit Tests (using pytest & tox)
* `make sdist` - Build a Python source distribution
* `make wheel` - Build a Python wheel
* `make artifacts` - Builds both sdist and wheel
* `make tox` - Run tests with ``tox`` to test against multiple Python versions
* `make mypy` - Run the static code analysis tool
* `make publish` - publish any artifacts in dist/* using twine
* `make format-code` - Format the code using the ``black`` formatter
* `make` - Equivalent to `make test sdist wheel`

## http://no-color.org/
Maagnar honors the ``NO_COLOR`` environment variable.


# Changelog

## 1.0.2
- Instead of using a set to track seen anagrams, store all seen values in a
  fanout cache on-disk; this reduces overall memory consumption though
  increases disk usage. (Issue #1)
- Added ``--clear-seen`` command line argument to start anagram generation over
  from scratch.

## 1.0.1
Add long description for pypi publication

## 1.0.0
Feature complete
