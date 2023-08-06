# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compai']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'compai',
    'version': '0.1.0',
    'description': 'Cool functional primitives to have',
    'long_description': None,
    'author': 'Fernando Martínez González',
    'author_email': 'frndmartinezglez@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
