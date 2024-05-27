# Useful tools for Python

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![tests](https://github.com/Rizhiy/replete/actions/workflows/test_and_version.yml/badge.svg)
[![codecov](https://codecov.io/gh/Rizhiy/replete/graph/badge.svg?token=FHM9FQ6IIU)](https://codecov.io/gh/Rizhiy/replete)
![publish](https://github.com/Rizhiy/replete/actions/workflows/publish.yml/badge.svg)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FRizhiy%2Freplete%2Fmaster%2Fpyproject.toml)
[![PyPI - Version](https://img.shields.io/pypi/v/replete)](https://pypi.org/project/replete/)

## Installation

Released version: `pip install replete`

## Development

- Install dev dependencies: `pip install -e ".[dev]"`
- For linting and basic fixes [ruff](https://docs.astral.sh/ruff/) is used: `ruff check . --fix`
- This repository follows strict formatting style which will be checked by the CI.
  - To format the code, use the [black](https://black.readthedocs.io) format: `black .`
  - To sort the imports, user [isort](https://pycqa.github.io/isort/) utility: `isort .`
- To test code, use [pytest](https://pytest.org): `pytest .`
- This repository follows semantic-release, which means all commit messages have to follow a [style](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html).
  You can use tools like [commitizen](https://github.com/commitizen-tools/commitizen) to write your commits.
- You can also use [pre-commit](https://pre-commit.com/) to help verify that all changes are valid.
  Multiple hooks are used, so use the following commands to install:

  ```bash
  pre-commit install
  pre-commit install --hook-type commit-msg
  ```
