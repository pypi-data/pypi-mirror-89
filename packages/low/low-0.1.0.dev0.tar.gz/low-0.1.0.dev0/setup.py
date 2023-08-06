# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['low']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'low',
    'version': '0.1.0.dev0',
    'description': 'A json parser',
    'long_description': 'Plum\n====\n\nA lightweight validation / constraint / coercion library\n',
    'author': 'Xavier Barbosa',
    'author_email': 'clint.northwood@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lab.errorist.xyz/py/plum',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
