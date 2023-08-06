# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alfalfa_client']

package_data = \
{'': ['*']}

install_requires = \
['pandas==0.24.2', 'requests-toolbelt==0.9.1']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'alfalfa-client',
    'version': '0.1.0.dev5',
    'description': 'A standalone client for the NREL Alfalfa application',
    'long_description': '# Alfalfa Client\n\nThe purpose of this repository is to provide a standalone client for use with the Alfalfa application.  It additionally includes a Historian to quickly/easily enable saving of results from Alfalfa simulations.\n\n# Usage\n\nThis repo is packaged and hosted on [PyPI here](https://pypi.org/project/alfalfa-client/).\n\n```bash\npip install alfalfa-client\n```\n\n```python\nimport alfalfa_client.alfalfa_client as ac\nimport alfalfa_client.historian as ah\n\nclient = ac.AlfalfaClient\nhistorian = ah.Historian\n```\n\n# Setup and Testing\nThis repository is setup to use:\n- [pyenv](https://github.com/pyenv/pyenv#installation) for managing python versions\n- [poetry](https://python-poetry.org/docs/#installation) for managing environment\n- [pre-commit](https://pre-commit.com/#install) for managing code styling\n- tox for running tests in isolated build environments.  See the expected python versions in [tox.ini](./tox.ini)\n\nAssuming poetry is installed and the necessary python versions are installed, the following should exit cleanly:\n```bash\ngit clone https://github.com/NREL/alfalfa-client.git\ncd alfalfa-client\npoetry run tox\n```\n\nThis may take some time resolving on the initial run, but subsequent runs should be faster.\n\nSee [this gist](https://gist.github.com/corymosiman12/26fb682df2d36b5c9155f344eccbe404) for additional info.\n\n\n# History\n- The implemented client is previously referred to as Boptest, from the alfalfa/client/boptest.py implementation.  It has been ported as a standalone package for easier usage across projects.\n\n# Releasing\n1. Merge all branches into develop, make sure tests pass\n1. Update the version (assume version is 0.1.2): `poetry version 0.1.2`\n1. Update the [version test](./tests/test_version.py) to match the above version\n1. Make sure tests pass: `poetry run tox`\n1. Merge develop into master, make sure tests pass\n1. Create a tag: `git tag 0.1.2`\n1. Build: `poetry build`\n1. Publish `poetry publish` (this will push to pypi)\n1. Create a new release on the Github repository using the tag and link to PyPI\n',
    'author': 'Kyle Benne',
    'author_email': 'kyle.benne@nrel.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
