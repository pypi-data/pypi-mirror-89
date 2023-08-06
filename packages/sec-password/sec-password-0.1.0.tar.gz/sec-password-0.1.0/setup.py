# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sec_password']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sec-password',
    'version': '0.1.0',
    'description': 'Secure Password library using only Python standard lib',
    'long_description': None,
    'author': 'Tom Faulkner',
    'author_email': 'tomfaulkner@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
