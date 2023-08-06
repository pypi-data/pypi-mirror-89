# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['good_guys', 'good_guys.layers']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'eyecu-good-guys',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
