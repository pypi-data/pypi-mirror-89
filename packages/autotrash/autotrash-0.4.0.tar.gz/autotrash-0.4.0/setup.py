# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['autotrash']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.17.0,<0.18.0']

entry_points = \
{'console_scripts': ['autotrash = autotrash.app:main']}

setup_kwargs = {
    'name': 'autotrash',
    'version': '0.4.0',
    'description': 'Script to automatically purge old trash',
    'long_description': None,
    'author': 'A. Bram Neijt',
    'author_email': 'bram@neijt.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
