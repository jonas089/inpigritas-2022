from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA384
import hashlib, time, os
from chainspec import RELATIVE_PATH
'''
    Manage asymmetric RSA keys
'''
class Keys:

    '''
        Initialise a new, empty Key instance
        :return: ()
        :rtype: ()
    '''
    def __init__(self):
        self.keys = None,
        self.passwd = None

    '''
        Create a new keypair and dump it as pem
        :return: ()
        :rtype: ()
    '''
    def new(self):
        self.keys = RSA.generate(2048)
        with open(RELATIVE_PATH + '/keys/private_key.pem', 'wb') as private_key_file:
            private_key_file.write(self.keys.exportKey('PEM', passphrase=self.passwd))
        with open(RELATIVE_PATH + '/keys/public_key.pem', 'wb') as public_key_file:
            public_key_file.write(self.keys.publickey().exportKey('PEM'))

    '''
        Get the active address for the active account
        :return: Address (= Hash of the public key)
        :rtype: str
    '''
    def get_address(self):
        publickey_str = str(self.public_key)
        _hash = hashlib.sha384()
        _hash.update(publickey_str.encode('utf-8'))
        return str(_hash.hexdigest())

    '''
        Read the active public key for the active account
        :return: Public key
        :rtype: RSA public key
    '''
    def public_key(self):
        with open(RELATIVE_PATH + '/keys/public_key.pem', 'r') as public_key_file:
            return RSA.importKey(public_key_file.read())

    '''
        Read the active private key for the active account
        :return: Private
        :rtype: RSA private key
    '''
    def private_key(self):
        with open(RELATIVE_PATH + '/keys/private_key.pem', 'r') as private_key_file:
            return RSA.importKey(private_key_file.read(), passphrase=self.passwd)

    '''
        Get the active public key as pem
        :return: Public key as pem
        :rtype: str
    '''
    def public_key_pem(self):
        with open(RELATIVE_PATH + '/keys/public_key.pem', 'r') as public_key_file:
            return public_key_file.read()

def tests():
    keypair = Keys()
    keypair.new()
    print(keypair.get_address())

#tests()
