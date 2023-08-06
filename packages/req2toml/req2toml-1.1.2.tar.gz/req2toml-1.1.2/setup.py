# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['req2toml']

package_data = \
{'': ['*']}

install_requires = \
['click==7.1.2', 'pytest-cov>=2.10.1,<3.0.0']

entry_points = \
{'console_scripts': ['req2lock = req2toml.console:cli']}

setup_kwargs = {
    'name': 'req2toml',
    'version': '1.1.2',
    'description': 'Convert requirements.txt to pyproject.toml',
    'long_description': '# Req2Toml\n\nAdding the dependencies from `requirements.txt` to `pyproject.toml` and `poetry.lock` with one command 😉\n\n\n\n## Install\n\n```bash\n$ pip install req2toml\n```\n\n\n\n## Usages\n\nThe entrypoint of the converter is `req2lock`\n\n#### Options\n\n- `-f` [required]  The  path to the `requirements.txt`\n- `--install` [optional] By default, it will only update the lock, add this flag to install the dependencies at the same time.\n- `-v`: Enable verbose mode to print out the debug logs\n\n\n\n```shell\n# Only update the poetry.lock\n$ req2lock -f requirements.txt\n\n# Install\n$ req2lock -f requirements.txt --install\n```\n\n\n\n## Contributing\n\nPR is always welcome <3\n',
    'author': 'Ben Chen',
    'author_email': 'benbenbang@github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benbenbang/req2toml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
