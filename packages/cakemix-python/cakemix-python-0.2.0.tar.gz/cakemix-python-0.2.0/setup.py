# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cakemix', 'cakemix.commands']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'SQLAlchemy-Utils>=0.36.8,<0.37.0',
 'SQLAlchemy>=1.3.22,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'questionary>=1.9.0,<2.0.0',
 'rich>=9.5.1,<10.0.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3.3.0,<4.0.0']}

entry_points = \
{'console_scripts': ['cakemix = cakemix.cli:cli']}

setup_kwargs = {
    'name': 'cakemix-python',
    'version': '0.2.0',
    'description': 'Cakemix is a tool for creating code template generators like create-react-app and npm-init. Avoiding you to waste time organizing a project.',
    'long_description': '==============\nCakemix :cake:\n==============\n\n|build| |codecov| |Gitpod ready to code|\n\nEnglish | Português_\n\nCakemix is a tool for creating code template generators like :code:`create-react-app` and :code:`npm init`. Avoiding you to waste time organizing a project.\n\n.. links\n\n.. _Português: ./locales/pt-br/README.rst\n\n.. images\n\n.. |build| image:: https://img.shields.io/github/workflow/status/vadolasi/cakemix/Python%20package\n   :alt: Tests status\n\n.. |codecov| image:: https://codecov.io/gh/vadolasi/cakemix/branch/master/graphs/badge.svg?branch=master\n   :alt: Code corverage status\n\n.. |Gitpod ready to code| image:: https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod\n   :alt: Open in Gitpod.io\n   :target: https://gitpod.io/#https://github.com/vadolasi/cakemix\n',
    'author': 'Vitor Daniel',
    'author_email': 'vitor036daniel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vadolasi/cakemix/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<=3.9.1',
}


setup(**setup_kwargs)
