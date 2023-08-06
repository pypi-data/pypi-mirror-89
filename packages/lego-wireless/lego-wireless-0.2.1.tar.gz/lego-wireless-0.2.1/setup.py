# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lego_wireless']

package_data = \
{'': ['*']}

install_requires = \
['blinker', 'gatt']

setup_kwargs = {
    'name': 'lego-wireless',
    'version': '0.2.1',
    'description': 'Control Lego Powered Up devices over Bluetooth',
    'long_description': '# Lego Wireless Protocol for Python\n\nA spare-time implementation of the Lego Wireless Protocol for Python, to support a pet project.\n\nSee `lego_wireless/__main__.py` for a usage example.\n',
    'author': 'Alex Dutton',
    'author_email': 'python-lego-wireless-protocol@alexdutton.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alexsdutton/python-lego-wireless-protocol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
