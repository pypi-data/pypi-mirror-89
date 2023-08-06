# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snipwizard', 'snipwizard.ds']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snipwizard',
    'version': '0.1.0',
    'description': 'A package that contains useful python utilities and snippets. Aims to have no dependencies on other python packages, just pure stdlib',
    'long_description': None,
    'author': 'Samuel DSR',
    'author_email': 'samuel.longshihe@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.0,<4.0',
}


setup(**setup_kwargs)
