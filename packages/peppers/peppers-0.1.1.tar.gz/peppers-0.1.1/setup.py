# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peppers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'peppers',
    'version': '0.1.1',
    'description': 'peppers for soup? Pyppers for Python!',
    'long_description': None,
    'author': 'innerNULL',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
