# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cakemix_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['cakemix = cakemix_python.cli:cli']}

setup_kwargs = {
    'name': 'cakemix-python',
    'version': '0.1.0',
    'description': 'Cakemix is a tool for creating code template generators like create-react-app and npm-init. Avoiding you to waste time organizing a project.',
    'long_description': '=======\nCakemix\n=======\n\n.. image:: https://img.shields.io/github/workflow/status/vadolasi/cakemix/Python%20package\n    :alt: Tests status\n\n.. image:: https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod\n    :alt: Open in Gitpod.io\n\nEnglish | `Português <./locales/pt-br/README.rst>`_\n\nCakemix is a tool for creating code template generators like create-react-app and npm-init. Avoiding you to waste time organizing a project.\n',
    'author': 'Vitor Daniel',
    'author_email': 'vitor036daniel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vadolasi/cakemix/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<=3.9',
}


setup(**setup_kwargs)
