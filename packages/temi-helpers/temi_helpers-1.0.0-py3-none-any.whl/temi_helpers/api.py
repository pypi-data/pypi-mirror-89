
# -*- coding: utf-8 -*-
from .bip38 import encrypt as encrypt_bip38
from .bip38 import decrypt as decrypt_bip38
from .utils import wif_encode

"""
bip38.api
~~~~~~~~~
:copyright: (c) 2020 by Junior Gantin.
:license: Apache2, see LICENSE for more details.
"""

def encrypt(private_key, passphrase):
    """Encrypts a private key with a passphrase, as specified in bip38.
    
    Args:  
        key (str|int|bytes): the private key to encrypt.
        passphrase (str): the passphrase that will be needed to decrypt the key.
        
    Returns:
        str: the encrypted private key.
    """
    if not isinstance(private_key, int) and not isinstance(private_key, str) and not isinstance(private_key, bytes):
        raise ValueError("<private_key> must be int bytes or str")
    if isinstance(private_key, str): # If a hex-key is passed as str
        try:
            if private_key[0] not in ["K", "L", "5"]:
                private_key = int(private_key, 16)
        except:
            raise ValueError(" if <key> is str it must be WIF encoded or an hex number")
    if not isinstance(passphrase, str):
        raise ValueError("<passphrase> must be str")
    return encrypt_bip38(private_key, passphrase) # type : str

def decrypt(private_key, passphrase):
    """Decrypts a bip38-encrypted Bitcoin private key.
    
    Args:
        key (str|int|byte): key to decrypt.
        passphrase (str): the passphrase used to encrypt the key.
        bin (bool): if True, returns the Bitcoin private key decrypted as bytes.
        
    Returns:
        int : the Bitcoin private key decrypted.
    """
    if not isinstance(private_key, int) and not isinstance(private_key, str) and not isinstance(private_key, bytes):
        raise ValueError("<private_key> must be int bytes or str")
    if isinstance(private_key, int): # If a hex-key is passed as str
        private_key = str(private_key)
    elif isinstance(private_key, bytes):
        private_key = str(int.from_bytes(private_key, 'big'))
    if not isinstance(passphrase, str):
        raise ValueError("<passphrase> must be str")
    decrypted = decrypt_bip38(private_key, passphrase)

    return wif_encode(decrypted)

