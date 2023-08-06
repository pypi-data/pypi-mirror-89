# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.10.0,<4.0.0',
 'requests>=2.24.0,<2.25.0',
 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=3.3.0,<4.0.0']}

entry_points = \
{'console_scripts': ['hypermodern-tutorial = '
                     'src.hypermodern_python.console:main']}

setup_kwargs = {
    'name': 'hypermodern-tutorial',
    'version': '0.1.2',
    'description': 'The hypermodern Python project - walking through tutorial',
    'long_description': '[![Tests](https://github.com/mattyocode/hypermodern-python-tutorial/workflows/Tests/badge.svg)](https://github.com/mattyocode/hypermodern-python-tutorial/actions?workflow=Tests)\n[![codecov](https://codecov.io/gh/mattyocode/hypermodern-python-tutorial/branch/main/graph/badge.svg?token=H8B46Y497K)](https://codecov.io/gh/mattyocode/hypermodern-python-tutorial)\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-tutorial.svg)](https://pypi.org/project/hypermodern-python/)\n\n\n# Working through Hypermodern Python tutorial/walk through\n\nTutorial found at: https://cjolowicz.github.io/posts/hypermodern-python-01-setup/\n',
    'author': 'mattyocode',
    'author_email': 'matthewoliver@live.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
