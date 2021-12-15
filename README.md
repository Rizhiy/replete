
[![pipeline status](http://192.168.135.11/utilities/nt-utils/badges/master/pipeline.svg)](http://192.168.135.11/utilities/nt-utils/commits/master)
[![coverage report](http://192.168.135.11/utilities/nt-utils/badges/master/coverage.svg)](http://192.168.135.11/utilities/nt-utils/commits/master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Installation

Released version: `pip install nt-utils`

Editable: use

```bash
pip install -U 'pip>=21.3.1' && \
git clone git@git@192.168.135.12:utilities/nt-utils && \
cd nt-utils && \
pip install -e '.[dev]'
```


## Development

### Formatting

This repository follows strict formatting style which will be checked by the CI.

To properly format the code, use the `nt-tools` package:
```bash
pip install nt-tools
nt-format
```

### Testing

Before pushing a commit, you can run `nt-test --format` which will try to
format the files and run tests.
