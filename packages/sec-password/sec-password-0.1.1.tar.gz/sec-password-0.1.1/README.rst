Secure Password Library using only Python standard lib
======================================================

A small Python library that aids in securely storing and authenticating passwords.

Based on best practice suggestions from:
https://crackstation.net/hashing-security.htm?=rd

Usage
-----

>>> hashed = hash_password(
...    password='secure password',
...    key='string from keyfile',
...    iterations=500
... )
>>> verify_password(
...    stored_password=hashed,
...    provided_password='secure password',
...    key='string from keyfile',
...    iterations=500
... )
True

Note that iterations is a multiplied by 1,000. 500 is probably a reasonable
default.

Keyed Hashes
------------

If ``key`` is used it should be a string read from a file or outside source that
is not stored in the database or hardcoded into the program.

Keyed Hashes are not required. By default an empty string is used.

See https://crackstation.net/hashing-security.htm?=rd for Keyed Hashes

Installation
------------

    poetry add sec-password

or

    pip install sec-password
