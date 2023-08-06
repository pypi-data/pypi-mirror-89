# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radcad']

package_data = \
{'': ['*']}

modules = \
['radCAD']
setup_kwargs = {
    'name': 'radcad',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Benjamin Scholtz',
    'author_email': 'ben@bitsofether.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
