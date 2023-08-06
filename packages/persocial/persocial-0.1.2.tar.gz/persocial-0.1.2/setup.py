# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['persocial', 'persocial.migrations', 'persocial.models']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.4,<4.0.0', 'wheel>=0.36.2,<0.37.0']

setup_kwargs = {
    'name': 'persocial',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Robert Townley',
    'author_email': 'me@roberttownley.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
