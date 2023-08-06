# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_microservice',
 'fast_microservice.routers',
 'fast_microservice.services',
 'fast_microservice.settings']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'fastapi>=0.63.0,<0.64.0',
 'pydantic>=1.7.3,<2.0.0',
 'python-multipart>=0.0.5,<0.0.6',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.25.1,<3.0.0',
 'sentry-sdk>=0.19.5,<0.20.0',
 'ujson>=4.0.1,<5.0.0',
 'uvicorn>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'fast-microservice',
    'version': '0.1.0rc4',
    'description': 'Small Microservice based on FastAPI',
    'long_description': '# fast-microservice\n\n![PyPI](https://img.shields.io/pypi/v/fast-microservice?style=flat-square)\n![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/jberends/fast-microservice/Test%20&%20Lint/master?style=flat-square)\n![Coveralls github branch](https://img.shields.io/coveralls/github/jberends/fast-microservice/master?style=flat-square)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fast-microservice?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/fast-microservice?style=flat-square)\n\nSmall Microservice Abased on FastAPI\n\n## Requirements\n\n* Python 3.6.1 or newer\n\n## Installation\n\n```sh\npip install fast-microservice\n```\n\n## Development\n\nThis project uses [poetry](https://poetry.eustace.io/) for packaging and\nmanaging all dependencies and [pre-commit](https://pre-commit.com/) to run\n[flake8](http://flake8.pycqa.org/), [isort](https://pycqa.github.io/isort/),\n[mypy](http://mypy-lang.org/) and [black](https://github.com/python/black).\n\nClone this repository and run\n\n```bash\npoetry install\npoetry run pre-commit install\n```\n\nto create a virtual enviroment containing all dependencies.\nAfterwards, You can run the test suite using\n\n```bash\npoetry run pytest\n```\n\nThis repository follows the [Conventional Commits](https://www.conventionalcommits.org/)\nstyle.\n',
    'author': 'Jochem Berends',
    'author_email': 'jberends@jbits.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jberends/fast-microservice',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
