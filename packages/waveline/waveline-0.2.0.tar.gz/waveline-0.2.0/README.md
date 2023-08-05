# WaveLine

[![CI](https://github.com/vallen-systems/pyWaveLine/workflows/CI/badge.svg)](https://github.com/vallen-systems/pyWaveLine/actions)
[![Documentation Status](https://readthedocs.org/projects/pywaveline/badge/?version=latest)](https://pywaveline.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/vallen-systems/pyWaveLine/badge.svg?branch=master)](https://coveralls.io/github/vallen-systems/pyWaveLine)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI](https://img.shields.io/pypi/v/wavepipe)](https://pypi.org/project/wavepipe)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wavepipe)](https://pypi.org/project/wavepipe)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Library to easily interface with Vallen Systeme WaveLine™ devices using the public APIs:

- conditionWave
- spotWave

## Documentation

For full documentation, please visit http://pywaveline.rtfd.io.

Check out the [examples](https://github.com/vallen-systems/pyWaveLine/tree/master/examples) for implementation details.

## Installation

Install the latest version from PyPI:

```
pip install waveline
```

Please note, that `waveline` requires Python 3.6 or newer. On Linux systems, `pip` is usually mapped to Python 2, so use `pip<version>` (e.g. `pip3` or `pip3.7`) instead. Alternatively, you can run `pip` from your specific Python version with `python<version> -m pip`.

## Contributing

Feature requests, bug reports and fixes are always welcome!

After cloning the repository, you can easily install the development environment and tools 
([pylint](https://www.pylint.org), [mypy](http://mypy-lang.org), [pytest](https://pytest.org), [tox](https://tox.readthedocs.io))
with:

```
git clone https://github.com/vallen-systems/pyWaveLine.git
cd pyWaveLine
pip install -e .[dev]
```

And run the test suite with tox:

```
tox
```

The documentation is built with [sphinx](https://www.sphinx-doc.org):

```
cd docs
sphinx-build . _build
```

### Run system tests

System level tests are only available, if the targeted device can be discovered.

Run system tests with a spotWave device:
```
pytest tests/system/spotwave --duration-acq 1
```
