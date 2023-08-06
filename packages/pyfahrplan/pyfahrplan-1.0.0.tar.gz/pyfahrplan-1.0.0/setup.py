# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfahrplan']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.22.0,<3.0.0',
 'requests_cache>=0.5.2,<0.6.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['pyfahrplan = pyfahrplan.pyfahrplan:cli']}

setup_kwargs = {
    'name': 'pyfahrplan',
    'version': '1.0.0',
    'description': 'A CCC Fahrplan CLI',
    'long_description': None,
    'author': 'Sascha',
    'author_email': 'saschalalala@github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
