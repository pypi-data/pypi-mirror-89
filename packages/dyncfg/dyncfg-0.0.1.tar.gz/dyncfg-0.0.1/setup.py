# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dyncfg', 'dyncfg.middleware']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'dyncfg',
    'version': '0.0.1',
    'description': 'Simples and powerful configuration engine',
    'long_description': None,
    'author': 'Rodrigo Pinheiro Matias',
    'author_email': 'rodrigopmatias@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
