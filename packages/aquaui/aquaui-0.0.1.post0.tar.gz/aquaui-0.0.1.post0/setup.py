# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aquaui']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aquaui',
    'version': '0.0.1.post0',
    'description': 'Native Mac OS UI elements with python',
    'long_description': '# Aqua UI',
    'author': 'ninest',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ninest/aquaui/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
