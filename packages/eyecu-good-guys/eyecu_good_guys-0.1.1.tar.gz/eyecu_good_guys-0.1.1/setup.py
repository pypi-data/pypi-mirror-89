# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eyecu_good_guys', 'eyecu_good_guys.layers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eyecu-good-guys',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
