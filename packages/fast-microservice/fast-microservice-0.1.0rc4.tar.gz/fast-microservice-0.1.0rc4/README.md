# fast-microservice

![PyPI](https://img.shields.io/pypi/v/fast-microservice?style=flat-square)
![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/jberends/fast-microservice/Test%20&%20Lint/master?style=flat-square)
![Coveralls github branch](https://img.shields.io/coveralls/github/jberends/fast-microservice/master?style=flat-square)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fast-microservice?style=flat-square)
![PyPI - License](https://img.shields.io/pypi/l/fast-microservice?style=flat-square)

Small Microservice Abased on FastAPI

## Requirements

* Python 3.6.1 or newer

## Installation

```sh
pip install fast-microservice
```

## Development

This project uses [poetry](https://poetry.eustace.io/) for packaging and
managing all dependencies and [pre-commit](https://pre-commit.com/) to run
[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),
[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).

Clone this repository and run

```bash
poetry install
poetry run pre-commit install
```

to create a virtual enviroment containing all dependencies.
Afterwards, You can run the test suite using

```bash
poetry run pytest
```

This repository follows the [Conventional Commits](https://www.conventionalcommits.org/)
style.
