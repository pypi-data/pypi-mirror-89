# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['req2toml']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2']

entry_points = \
{'console_scripts': ['req2lock = req2toml.console:cli']}

setup_kwargs = {
    'name': 'req2toml',
    'version': '1.1.0',
    'description': 'Convert requirements.txt to pyproject.toml',
    'long_description': None,
    'author': 'Ben Chen',
    'author_email': 'benbenbang@github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
