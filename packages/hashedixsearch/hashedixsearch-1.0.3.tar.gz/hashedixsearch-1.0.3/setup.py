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
    'version': '1.0.3',
    'description': 'in-process search-engine for python',
    'long_description': "# hashedixsearch\n\n`hashedixsearch` is a lightweight in-process search engine for Python, with support for stemming, synonyms, custom token analyzers, and query match highlighting.\n\n## Usage\n\n```python\nfrom hashedixsearch import HashedIXSearch\n\nindex = HashedIXSearch(synonyms={'search': 'find'})\nindex.add(\n    doc_id=1,\n    doc='find the needle in the haystack'\n)\n\nresults = index.query_batch(['search'])\nfor query, hits in results:\n    print(f'{query}: {hits}')\n```\n\n## Tests\n\nTo run the `hashedixsearch` test suite:\n\n```bash\n$ python -m unittest\n```\n\nThis library uses [hashedindex](https://github.com/MichaelAquilina/hashedindex) for tokenization and indexing.\n",
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
