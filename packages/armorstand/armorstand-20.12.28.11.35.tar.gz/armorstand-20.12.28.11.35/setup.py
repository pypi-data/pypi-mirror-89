# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['armorstand']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'armorstand',
    'version': '20.12.28.11.35',
    'description': 'All my utility functions',
    'long_description': None,
    'author': 'ninest',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
