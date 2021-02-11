PYTHON=python3
ENV_DIR=.env_$(PYTHON)
MAKEFILE_DIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))

ifeq ($(OS),Windows_NT)
	MAKE_FOLDER=$(CURDIR)
	IN_ENV=. $(ENV_DIR)/Scripts/activate &&
else
	MAKE_FOLDER := $(shell pwd)
	IN_ENV=. $(ENV_DIR)/bin/activate &&
endif

all: test sdist

env: $(ENV_DIR)
	$(IN_ENV) pip install -U pip

# Static Analysis
mypy:
	$(IN_ENV) mypy --ignore-missing-imports src

# Invoke tox to test multiple python versions
tox:
	$(IN_ENV) tox --skip-missing-interpreters

# Quick test invoke
qt: check-code
	$(IN_ENV) pytest tests

test: build qt mypy

artifacts: build wheel sdist

$(ENV_DIR):
	virtualenv -p $(PYTHON) $(ENV_DIR)

build-reqs: env
	$(IN_ENV) pip install 'black==20.8b1' pytest mypy twine tox

build: build-reqs
	$(IN_ENV) pip install -U --pre --editable .

sdist: build
	$(IN_ENV) python setup.py sdist

wheel: build-reqs
	$(IN_ENV) python setup.py bdist_wheel

publish: artifacts
	$(IN_ENV) twine upload dist/*

format-code:
	$(IN_ENV) black -l 119 src/ tests/ setup.py

check-code:
	$(IN_ENV) black --check -l 119 src/ tests/ setup.py

freeze: env
	- $(IN_ENV) pip freeze

shell: env
	- $(IN_ENV) $(PYTHON)

clean:
	- @rm -rf BUILD
	- @rm -rf BUILDROOT
	- @rm -rf RPMS
	- @rm -rf SRPMS
	- @rm -rf SOURCES
	- @rm -rf docs/build
	- @rm -rf src/*.egg-info
	- @rm -rf build
	- @rm -rf dist
	- @rm -rf docs/_build
	- @rm -rf docs/build
	- @rm -f .coverage
	- @rm -f test_results.xml
	- @rm -f coverage.xml
	- @rm -f pep8.out
	- @rm -f tests/coverage.xml
	- @rm -f docs/*.medusa-changelog.json
	- @find . -name '*.orig' -delete
	- @find . -name '*.DS_Store' -delete
	- @find . -name '*.pyc' -delete
	- @find . -name '*.pyd' -delete
	- @find . -name '*.pyo' -delete
	- @find . -name '*__pycache__*' -delete

env-clean: clean
	- @rm -rf .env_python*
	- @git clean -dfX
	- @rm -rf $(ENV_DIR)
