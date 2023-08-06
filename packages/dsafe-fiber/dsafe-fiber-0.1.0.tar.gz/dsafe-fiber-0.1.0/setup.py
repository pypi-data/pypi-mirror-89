# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fiber',
 'fiber.client',
 'fiber.crud',
 'fiber.models',
 'fiber.schemas',
 'fiber.schemas.orm']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.22,<2.0.0',
 'psycopg2-binary>=2.8.6,<3.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'sqlalchemy-stubs>=0.3,<0.4']

setup_kwargs = {
    'name': 'dsafe-fiber',
    'version': '0.1.0',
    'description': 'Smart Contract Monitoring SDK',
    'long_description': 'Fiber\n=====\n\n![ci checks](https://github.com/dsafe/fiber/workflows/ci/badge.svg)\n\n**A SDK for monitoring smart contracts**\n',
    'author': 'Robin Raymond',
    'author_email': 'robin@robinraymond.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
