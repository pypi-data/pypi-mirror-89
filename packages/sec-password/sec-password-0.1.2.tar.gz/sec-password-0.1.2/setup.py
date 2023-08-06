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
    'version': '0.1.2',
    'description': 'Secure Password library using only Python standard lib',
    'long_description': "Secure Password Library using only Python standard lib\n======================================================\n\nA small Python library that aids in securely storing and authenticating passwords.\n\nBased on best practice suggestions from:\nhttps://crackstation.net/hashing-security.htm?=rd\n\nUsage\n-----\n\n>>> hashed = hash_password(\n...    password='secure password',\n...    key='string from keyfile',\n...    iterations=500\n... )\n>>> verify_password(\n...    stored_password=hashed,\n...    provided_password='secure password',\n...    key='string from keyfile',\n...    iterations=500\n... )\nTrue\n\nNote that iterations is a multiplied by 1,000. 500 is probably a reasonable\ndefault.\n\nKeyed Hashes\n------------\n\nIf ``key`` is used it should be a string read from a file or outside source that\nis not stored in the database or hardcoded into the program.\n\nKeyed Hashes are not required. By default an empty string is used.\n\nSee https://crackstation.net/hashing-security.htm?=rd for Keyed Hashes\n\nInstallation\n------------\n\n    poetry add sec-password\n\nor\n\n    pip install sec-password\n",
    'author': 'Tom Faulkner',
    'author_email': 'tomfaulkner@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TomFaulkner/sec-password',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
