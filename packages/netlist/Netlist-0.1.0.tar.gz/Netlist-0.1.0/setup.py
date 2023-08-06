# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netlist']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'netlist',
    'version': '0.1.0',
    'description': 'Circuit Netlist Generation and Parsing',
    'long_description': None,
    'author': 'Dan Fritchman',
    'author_email': 'dan@fritch.mn',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
