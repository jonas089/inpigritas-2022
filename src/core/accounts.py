from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA384
import hashlib, time, os
from chainspec import RELATIVE_PATH
'''
    * Manage asymmetric RSA keys
'''
class Keys:
    def __init__(self):
        self.keys = None,
        self.passwd = None

    '''
        * Create a new asymmetric keypair
    '''
    def new(self):
        self.keys = RSA.generate(2048)
        with open(RELATIVE_PATH + '/keys/private_key.pem', 'wb') as private_key_file:
            private_key_file.write(self.keys.exportKey('PEM', passphrase=self.passwd))
        with open(RELATIVE_PATH + '/keys/public_key.pem', 'wb') as public_key_file:
            public_key_file.write(self.keys.publickey().exportKey('PEM'))

    '''
        * Address (a hash of the public key)
    '''
    def get_address(self):
        publickey_str = str(self.public_key)
        _hash = hashlib.sha384()
        _hash.update(publickey_str.encode('utf-8'))
        return str(_hash.hexdigest())

    '''
        * Public Key
    '''
    def public_key(self):
        with open(RELATIVE_PATH + '/keys/public_key.pem', 'r') as public_key_file:
            return RSA.importKey(public_key_file.read())

    '''
        * Private Key
    '''
    def private_key(self):
        with open(RELATIVE_PATH + '/keys/private_key.pem', 'r') as private_key_file:
            return RSA.importKey(private_key_file.read(), passphrase=self.passwd)

    '''
        * Export public key for signature verification
    '''
    def public_key_pem(self):
        with open(RELATIVE_PATH + '/keys/public_key.pem', 'r') as public_key_file:
            return public_key_file.read()

def tests():
    keypair = Keys()
    keypair.new()
    print(keypair.get_address())

#tests()
