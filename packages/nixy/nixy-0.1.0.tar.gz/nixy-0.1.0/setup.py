# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nixy']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'nixy',
    'version': '0.1.0',
    'description': 'Python bindings for Nix package manager and nix-user-chroot',
    'long_description': None,
    'author': 'Anna Rogers',
    'author_email': 'arogers@sodas.ku.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
