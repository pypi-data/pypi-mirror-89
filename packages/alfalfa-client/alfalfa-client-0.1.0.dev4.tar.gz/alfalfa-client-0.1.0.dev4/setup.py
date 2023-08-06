# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alfalfa_client']

package_data = \
{'': ['*']}

install_requires = \
['pandas==0.24.2', 'requests-toolbelt==0.9.1']

setup_kwargs = {
    'name': 'alfalfa-client',
    'version': '0.1.0.dev4',
    'description': 'A standalone client for the NREL Alfalfa application',
    'long_description': '# Alfalfa Client\n\nThe purpose of this repository is to provide a standalone client for use with the Alfalfa application.  It additionally includes a Historian to quickly/easily enable saving of results from Alfalfa simulations.\n\n# Usage\n\nThis repo is packaged and hosted on PyPI.\n\n```\npip install alfalfa-client\nfrom alfalfa_client import AlfalfaClient, Historian\n```\n\n# History\n- The implemented client is previously referred to as Boptest, from the alfalfa/client/boptest.py implementation.  It has been ported as a standalone package for easier usage across projects.\n',
    'author': 'Kyle Benne',
    'author_email': 'kyle.benne@nrel.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
