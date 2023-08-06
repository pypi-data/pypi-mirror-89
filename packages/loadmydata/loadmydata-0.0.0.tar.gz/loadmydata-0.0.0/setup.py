# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loadmydata']

package_data = \
{'': ['*']}

install_requires = \
['pandas', 'requests', 'sktime', 'tqdm', 'yarl']

setup_kwargs = {
    'name': 'loadmydata',
    'version': '0.0.0',
    'description': 'Collections of utility functions to download open-source data sets.',
    'long_description': None,
    'author': 'Charles T.',
    'author_email': 'charles@doffy.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
