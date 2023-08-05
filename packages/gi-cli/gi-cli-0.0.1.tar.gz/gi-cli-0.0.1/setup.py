# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gi_cli']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.15.0,<0.16.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['gi = gi-cli.__main__:main']}

setup_kwargs = {
    'name': 'gi-cli',
    'version': '0.0.1',
    'description': 'CLI to easily create .gitignore files',
    'long_description': None,
    'author': 'ninest',
    'author_email': None,
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
