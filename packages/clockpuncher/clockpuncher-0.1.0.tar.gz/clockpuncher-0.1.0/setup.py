# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clockpuncher', 'clockpuncher.gui', 'clockpuncher.tests']

package_data = \
{'': ['*'], 'clockpuncher': ['data/*', 'fonts/*']}

install_requires = \
['dataset>=1.4.1,<2.0.0', 'dearpygui>=0.6.42,<0.7.0', 'pandas>=1.1.5,<2.0.0']

entry_points = \
{'console_scripts': ['clockpuncher = clockpuncher.main:main']}

setup_kwargs = {
    'name': 'clockpuncher',
    'version': '0.1.0',
    'description': 'A hackable GUI time tracker designed to be easily modified for user-centric automation.',
    'long_description': None,
    'author': 'Erin Maestas',
    'author_email': 'ErinLMaestas@gmail.com',
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
