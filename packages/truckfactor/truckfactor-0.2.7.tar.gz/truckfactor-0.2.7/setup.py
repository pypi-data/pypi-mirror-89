# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['truckfactor']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'numpy>=1.19.4,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['truckfactor = truckfactor.compute:run']}

setup_kwargs = {
    'name': 'truckfactor',
    'version': '0.2.7',
    'description': ' Tool to compute the truck factor of a Git repository ',
    'long_description': 'uiuiui\n',
    'author': 'HelgeCPH',
    'author_email': 'ropf@itu.dk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HelgeCPH/truckfactor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
