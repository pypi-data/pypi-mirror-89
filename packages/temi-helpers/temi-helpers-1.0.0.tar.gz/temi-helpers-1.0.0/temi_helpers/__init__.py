# -*- coding: utf-8 -*-

"""
Bip38 library
~~~~~~~~~~~~~
Bip38 is a library, written in Python, to secure your Bitcoin private keys.
# Full specification https://github.com/bitcoin/bips/blob/master/bip-0038.mediawiki
Usage:
   >>> from temi_helpers import encrypt, decrypt
   >>> encrypt(private_key, passphrase)
   6P
   >>> decrypt(private_key, passphrase)
   WIF
:copyright: (c) 2020 by Junior Gantin.
:license: Apache 2.0, see LICENSE for more details.
"""

from .api import encrypt, decrypt