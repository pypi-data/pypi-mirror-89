# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gi_cli']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.15.0,<0.16.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['gi = gi_cli.__main__:main',
                     'gitignore = gi_cli.__main__:main']}

setup_kwargs = {
    'name': 'gi-cli',
    'version': '0.0.4',
    'description': 'CLI to easily create .gitignore files',
    'long_description': '# gi\n\n> Easily create a .gitignore\n\n![PyPI](https://img.shields.io/pypi/v/gi-cli?style=flat-square)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/gi-cli?style=flat-square)\n![GitHub](https://img.shields.io/github/license/ninest/gi?style=flat-square)\n\n## Usage\n\n```bash\n# Install it\n$ pip install gi-cli\n\n# Add a language framework\n$ gi add python\n\n# Or add multiple\n$ git add node python\n\n# Clear your gitignore\n$ git clear\n\n# Uninstall it\n$ pip uninstall gi-cli\n```\n\n**Note**: Mac or Linux users may have to use `pip3` instead of `pip`.\n\n## Build setup\n\nClone or fork the repository, then run the commands:\n\n```bash\npoetry shell\npoetry install\n```\n\nAdd the pre-commit hooks:\n\n```bash\npre-commit install\n```\n\n### Editor settings\n\n```json\n{\n  "python.formatting.provider": "black",\n  "editor.formatOnSave": true,\n  "[python]": {\n    "editor.insertSpaces": true,\n    "editor.detectIndentation": false,\n    "editor.tabSize": 4\n  },\n  "python.linting.enabled": true,\n  "python.linting.flake8Enabled": true,\n  "python.linting.pylintEnabled": false,\n\n  "python.pythonPath": "/Users/username-here/Library/Caches/pypoetry/virtualenvs/xxx-py3.7"\n}\n```\n\n## License\n\nMIT\n',
    'author': 'ninest',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ninest/gi/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
