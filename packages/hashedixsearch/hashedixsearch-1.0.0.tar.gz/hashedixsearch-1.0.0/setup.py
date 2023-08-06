# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hashedixsearch']

package_data = \
{'': ['*']}

install_requires = \
['hashedindex>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'hashedixsearch',
    'version': '1.0.0',
    'description': 'in-process search-engine for python',
    'long_description': None,
    'author': 'James Addison',
    'author_email': 'james@reciperadar.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/openculinary/hashedixsearch/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
