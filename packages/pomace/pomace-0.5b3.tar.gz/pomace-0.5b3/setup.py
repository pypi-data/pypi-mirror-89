# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pomace', 'pomace.tests']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.8.2,<5.0.0',
 'bullet>=2.1.0,<3.0.0',
 'cleo>=0.8.1,<0.9.0',
 'datafiles==0.11b4',
 'faker>=4.1.1,<5.0.0',
 'inflection>=0.4.0,<0.5.0',
 'ipython>=7.12.0,<8.0.0',
 'minilog>=2.0b2,<3.0',
 'parse>=1.14.0,<2.0.0',
 'splinter>=0.12.0,<0.13.0',
 'webdriver_manager>=2.5.0,<3.0.0',
 'zipcodes>=1.1.2,<2.0.0']

entry_points = \
{'console_scripts': ['pomace = pomace.cli:application.run']}

setup_kwargs = {
    'name': 'pomace',
    'version': '0.5b3',
    'description': 'Dynamic page objects for browser automation.',
    'long_description': '# Overview\n\nDynamic page objects for browser automation.\n\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).\n\n[![Unix Build Status](https://img.shields.io/travis/jacebrowning/pomace/main.svg?label=unix)](https://travis-ci.org/jacebrowning/pomace)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/pomace/main.svg?label=window)](https://ci.appveyor.com/project/jacebrowning/pomace)\n[![Coverage Status](https://img.shields.io/coveralls/jacebrowning/pomace/main.svg)](https://coveralls.io/r/jacebrowning/pomace)\n[![PyPI Version](https://img.shields.io/pypi/v/pomace.svg)](https://pypi.org/project/pomace)\n[![PyPI License](https://img.shields.io/pypi/l/pomace.svg)](https://pypi.org/project/pomace)\n\n# Setup\n\n## Requirements\n\n- Python 3.7+\n\n## Installation\n\nOn macOS:\n\n```\n$ brew install pipx\n$ pipx ensurepath\n$ pipx install pomace\n$ pomace shell\n$ pomace run\n```\n',
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pomace',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
