# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mserv', 'mserv.Libs', 'mserv.UI']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.15.2,<6.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'requests>=2.25.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.54.1,<5.0.0']

entry_points = \
{'console_scripts': ['mserv = mserv.mserv:mserv_cli']}

setup_kwargs = {
    'name': 'mserv',
    'version': '0.8',
    'description': 'A rough server manager for Minecraft',
    'long_description': None,
    'author': 'Quinton Jasper',
    'author_email': 'dropatuningmetal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
