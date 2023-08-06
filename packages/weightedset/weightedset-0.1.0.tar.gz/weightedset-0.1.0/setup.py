# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['weightedset']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'weightedset',
    'version': '0.1.0',
    'description': 'Weighted set',
    'long_description': '# weightedset\nWeighted Set implementation for Python\n',
    'author': 'Gary Donovan',
    'author_email': 'gazza@gazza.id.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Oovvuu/weightedset',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
