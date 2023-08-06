# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncalchemy']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'asyncalchemy',
    'version': '1.0.0',
    'description': 'A thin async wrapper for SQLAlchemy sessions.',
    'long_description': None,
    'author': 'Shaul Kramer',
    'author_email': 'shaulkr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/claroty/AsyncAlchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
