[![pipeline status](https://gitlab.com/neurotrade1/utils/nt-utils/badges/master/pipeline.svg)](https://gitlab.com/neurotrade1/utils/nt-utils/-/commits/master)
[![coverage report](https://gitlab.com/neurotrade1/utils/nt-utils/badges/master/coverage.svg)](https://gitlab.com/neurotrade1/utils/nt-utils/-/commits/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Installation

Released version: `pip install nt-utils`

## Development

Editable installation:

```bash
pip install -U 'pip>=21.3.1' && \
git clone git@git@192.168.135.12:utilities/nt-utils && \
cd nt-utils && \
pip install -e '.[dev,tests]'
```

### Formatting

This repository follows strict formatting style which will be checked by the CI.

To properly format the code, use the `nt-dev` package:

```bash
pip install nt-dev
nt-format
```

### Testing

Before pushing a commit, you can run `nt-test --format` which will try to
format the files and run tests.

This project is _preferentially_ `mypy --strict` typed, without enforcement in CI.
