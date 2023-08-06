"""
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
"""


__version__ = "0.1.0"


import binascii
import doctest
import hashlib
import os


def _hash(password:str, salt:str, key:str, iterations: int):
    pwdhash = hashlib.pbkdf2_hmac(
        "sha512", password.encode("utf-8"), salt + key.encode(), 1000 * iterations
    )
    return binascii.hexlify(pwdhash)


def hash_password(
    password: str, key: str = "", iterations: int = 500
) -> str:
    """Hash a password for storing.

    Returns hashed password.
    """
    salt = hashlib.sha512(os.urandom(60)).hexdigest().encode("ascii")
    pwdhash = _hash(password, salt, key, iterations)
    return (salt + pwdhash).decode("ascii")


def verify_password(
    stored_password: str, provided_password: str, key: str = "", iterations: int = 500
) -> bool:
    """Verify a stored password against one provided by user"""
    salt = stored_password[:128].encode()
    stored_password = stored_password[128:].encode()
    pwdhash = _hash(provided_password, salt, key, iterations)
    return pwdhash == stored_password


if __name__ == '__main__':
    doctest.testmod()
