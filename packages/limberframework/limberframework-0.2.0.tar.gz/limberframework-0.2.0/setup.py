# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['limberframework',
 'limberframework.authentication',
 'limberframework.cache',
 'limberframework.config',
 'limberframework.database',
 'limberframework.filesystem',
 'limberframework.foundation',
 'limberframework.hashing',
 'limberframework.routing',
 'limberframework.support']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0',
 'aioredlock>=0.5.2,<0.6.0',
 'fastapi==0.59.0',
 'psycopg2==2.8.5',
 'pydantic==1.6.1',
 'pymemcache==3.2.0',
 'redis==3.5.3',
 'sqlalchemy==1.3.18']

setup_kwargs = {
    'name': 'limberframework',
    'version': '0.2.0',
    'description': 'The core of the Limber Framework, a python web application framework built using FastAPI.',
    'long_description': '# README\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)\n[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODEOFCONDUCT.md)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n> Note: This repository contains the core code of the Limber Framework. If you want to build an application using Limber, visit the main Limber repository.\n\nLimber Framework is a web application framework with the goal of simplifying the development of web applications. It is based on the FastAPI framework and provides utilities to handle common tasks performed when developing web applications.\n\n## Contributing\nThank you for considering contributing to the Limber Framework! The contribution guide can be found in the [here](CONTRIBUTING.md).\n\n## Code of Conduct\nTo ensure that the Limber community is welcoming to all, please review and abide by the [Code of Conduct](CODEOFCONDUCT.md).\n\n## License\nThe Limber Framework is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).',
    'author': 'Jonathan Staniforth',
    'author_email': 'jonathanstaniforth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/limber-project/limberframework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.9.0',
}


setup(**setup_kwargs)
