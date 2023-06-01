import os, hashlib, pickle, time, base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA384
from core.accounts import Keys
from core.blockchain import Blockchain
from chainspec import RELATIVE_PATH

'''
    Transfer object used to construct and dispatch a transaction
'''
class Transfer():

    '''
        Initialise a new Transfer
        :param: sender
        :type sender: str
        :param: recipient
        :type recipient: str
        :param: amount
        :type amount: float
        :param: timestamp
        :type timestamp: str
        :param: tx_hash
        :type tx_hash: str
        :param: signature
        :type signature: RSA signature
        :param: public_key_pem
        :type public_key_pem: str
        :param: height
        :type height: int
        :param: keypair
        :type keypair: RSA keypair
        :return: ()
        :rtype: ()
    '''
    def __init__(self, sender, recipient, amount, timestamp, tx_hash, signature, public_key_pem, height, keypair):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp
        self.transaction_hash = tx_hash
        self.signature = signature
        self.public_key_pem = public_key_pem
        self.Keys = keypair
        self.height = height

    '''
        Create a new Transfer with signature
        :return: ()
        :rtype: ()
    '''
    def new(self):
        # public_key_pem: export
        self.public_key_pem = self.Keys.public_key_pem()
        self.timestamp = time.time()
        tx = '{sender}{recipient}{amount}{timestamp}{public_key_pem}'.format(sender=self.sender, recipient=self.recipient, amount=self.amount, timestamp=self.timestamp, public_key_pem=self.Keys.public_key_pem())
        _hash = SHA384.new()
        _hash.update(tx.encode('utf-8'))
        self.transaction_hash = str(_hash.hexdigest())
        cypher = PKCS1_v1_5.new(self.Keys.private_key())
        signature = cypher.sign(_hash)
        self.signature = base64.b64encode(signature).decode('utf-8')

    '''
        Represent the Transfer as json
        :return: ()
        :rtype: ()
    '''
    def finalize(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'transaction_hash': self.transaction_hash,
            'signature': self.signature,
            'public_key': self.public_key_pem
        }

    '''
        Add the Transfer to the selected transaction pool
        :param: height
        :type height: int
        :return: ()
        :rtype: ()
    '''
    def add_to_pool(self, height):
        is_empty_pool = False
        if not os.path.exists(RELATIVE_PATH + '/txpool'):
            os.mkdir(RELATIVE_PATH + '/txpool')
        if not os.path.exists(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=height)):
            is_empty_pool = True
            open(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=height), 'x')

        # backup if not empty
        pool = []
        if is_empty_pool == False:
            with open(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=height), 'rb') as pool_file:
                pool = pickle.load(pool_file)
        # validate first.
        pool.append(self.finalize())
        with open(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=height), 'wb') as pool_file:
            pickle.dump(pool, pool_file)

    '''
        Validate a Transfer and it's signature
        :param: instance
        :type instance: Blockchain
        :return: Validation result
        :rtype: bool
    '''
    def validate(self, instance):
        # perform balance checks locally
        '''
            ... TBD ...
        '''
        # timestamp
        if not self.timestamp < instance.last_block_timestamp():
            return '[Error]: Timestamp not valid for current Block'
        '''
            ... TBD ...
        '''
        # validate signature
        signature = base64.b64decode(self.signature.encode('utf-8'))
        tx = '{sender}{recipient}{amount}{timestamp}{public_key_pem}'.format(sender=self.sender, recipient=self.recipient, amount=self.amount, timestamp=self.timestamp, public_key_pem=self.public_key_pem)
        _hash = SHA384.new()
        _hash.update(tx.encode('utf-8'))
        cypher = PKCS1_v1_5.new(RSA.importKey(self.public_key_pem))
        # verify
        return cypher.verify(_hash, signature)

'''
def tests():
    tx = Transfer('sender', 'recipient', 10, None, None, None, None)
    tx.new()
    tx.add_to_pool(0)
    print(tx.finalize())
#tests()
'''
