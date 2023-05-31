import os, time, hashlib, pickle, base64
from chainspec import ACCOUNT, PREMINE, BLOCKTIME, RELATIVE_PATH
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA384

'''
    * Prototype Blockchain class and 'database'
'''
class Blockchain():

    '''
        * Initialise an existing or empty Inpigritas Blockchain
    '''
    def __init__(self):
        self.chain = []
        self.update()

    '''
        * Create a new blockchain data file
    '''
    def new(self):
        if not os.path.exists(RELATIVE_PATH + '/data/blockchain.dat'):
            open(RELATIVE_PATH + '/data/blockchain.dat', 'x')
        else:
            os.remove(RELATIVE_PATH + '/data/blockchain.dat')
            open(RELATIVE_PATH + '/data/blockchain.dat', 'x')

    '''
        * Re-load the current blockchain data file
        * Respond to changes
    '''
    def update(self):
        try:
            with open(RELATIVE_PATH + '/data/blockchain.dat', 'rb') as chain_file:
                self.chain = pickle.load(chain_file)
        except Exception as empty:
            self.chain = []

    '''
        * Read the current blockchain data file
    '''
    def read(self):
        with open(RELATIVE_PATH + '/data/blockchain.dat', 'rb') as chain_file:
            return pickle.load(chain_file)

    '''
        * Write to the current blockchain data file
    '''
    def write(self):
        with open(RELATIVE_PATH + '/data/blockchain.dat', 'wb') as chain_file:
            pickle.dump(self.chain, chain_file)
        self.update()

    '''
        * Delete the current blockchain data file
    '''
    def teardown(self):
        if os.path.exists(RELATIVE_PATH + '/data/blockchain.dat'):
            os.remove(RELATIVE_PATH + '/data/blockchain.dat')

    '''
        * Add a new block to the blockchain datafile
    '''
    def add_finalized_block(self, Block):
        # Read txpool for current Block and append transactions
        if os.path.exists(RELATIVE_PATH + '/txpool/{index}.dat'.format(index=Block['index'])):
            with open(RELATIVE_PATH + '/txpool/{index}.dat'.format(index=Block['index']), 'rb') as pool_file:
                try:
                    Block['transfers'] = [*Block['transfers'], *pickle.load(pool_file)]
                except Exception as Empty:
                    Block['transfers'] = [*Block['transfers'], *[]]
                os.remove(RELATIVE_PATH + '/txpool/{index}.dat'.format(index=Block['index']))
        self.chain.append(Block)
        self.write()

    '''
        * Add a block received from a peer through synchronisation
    '''
    def add_external_finalized_block(self, Block):
        self.chain.append(Block)
        self.write()
        if os.path.exists(RELATIVE_PATH + '/txpool/{index}.dat'.format(index=Block['index'])):
            os.remove(RELATIVE_PATH + '/txpool/{index}.dat'.format(index=Block['index']))

    '''
        * Validate the data integrity of a block
        * Verify the hash and height
    '''
    def validate(self, _Block, allow_future_blocks):
        # Block can not be in the future
        if _Block.timestamp > time.time() and allow_future_blocks == False:
            return False
        prev_Block_Dict = self.chain[_Block.index - 1]
        prev_Block = Block(prev_Block_Dict['index'], prev_Block_Dict['timestamp'], prev_Block_Dict['next_timestamp'], prev_Block_Dict['block_hash'], prev_Block_Dict['next_hash'], prev_Block_Dict['prev_hash'], prev_Block_Dict['transfers'])
        # compare Blocks
        if prev_Block.hash != _Block.prev_hash or prev_Block.next_hash != _Block.hash or prev_Block.index != (_Block.index - 1) or prev_Block.next_timestamp != _Block.timestamp:
            return False
        # validate Block hash
        block_hash = hashlib.sha384()
        block_hash.update('{index}{prev_hash}{timestamp}'.format(index=_Block.index, prev_hash=_Block.prev_hash, timestamp=_Block.timestamp).encode('utf-8'))
        _hash = str(block_hash.hexdigest())
        if _hash != _Block.hash or _hash != prev_Block.next_hash:
            return False
        # validate Transfers in Block using Transfer class
        return True

    '''
        * Retrieve the height of the next block to be created
    '''
    def height(self):
        return len(self.chain) + 1

    '''
        * Retrieve the timestamp of the next block to be created
    '''
    def next_block_timestamp(self):
        return self.chain[-1]['next_timestamp']

    '''
        * Retrieve the height of the last block that has been added to the chain
    '''
    def last_block_timestamp(self):
        return self.chain[-1]['timestamp']

    '''
        * Create a new block using the time-based consensus protocol
    '''
    def create_next_block(self):
        prev_Block_Dict = self.chain[-1]
        prev_Block = Block(prev_Block_Dict['index'], prev_Block_Dict['timestamp'], prev_Block_Dict['next_timestamp'], prev_Block_Dict['block_hash'], prev_Block_Dict['next_hash'], prev_Block_Dict['prev_hash'], prev_Block_Dict['transfers'])
        next_Block = Block(None, None, None, None, None, None, [])
        next_Block.new(prev_Block)
        self.add_finalized_block(next_Block.finalize())

    '''
        * Read the current transaction pool
    '''
    def txpool(self):
        if not os.path.exists(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=self.height())):
            return []
        else:
            with open(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=self.height()), 'rb') as pool_file:
                return pickle.load(pool_file)

    '''
        * Check for a duplicate transaction in the current transaction pool
    '''
    def is_duplicate_in_pool(self, tx):
        local_pool = self.txpool()
        if len(local_pool) != 0:
            for _tx in local_pool:
                if tx['transaction_hash'] == _tx['transaction_hash']:
                    return True
        return False

'''
    * Block as an object with attributes and methods
'''
class Block():
    '''
        * Initialise a block from parameters
    '''
    def __init__(self, index, timestamp, next_timestamp, block_hash, next_hash, prev_hash, transfers):
        self.index = index
        self.timestamp = timestamp
        self.next_timestamp = next_timestamp
        self.hash = block_hash
        self.next_hash = next_hash
        self.prev_hash = prev_hash
        self.transfers = transfers

    '''
        * Create a new block based on a previous block
        * Deduce whether the block is a genesis block and use default parameters in that case
    '''
    def new(self, prev_Block):
        if prev_Block == None:
            self.index = 0
        else:
            self.index = prev_Block.index + 1
        if self.index != 0:
            self.prev_hash = prev_Block.hash
            self.timestamp = prev_Block.next_timestamp
        else:
            # Genesis Block
            self.transfers.append(
                # Genesis Transaction
                {
                    'sender':'0x00',
                    'recipient':ACCOUNT,
                    'amount':PREMINE,
                    'timestamp': time.time()
                }
            )
            self.timestamp = time.time()
        self.next_timestamp = self.timestamp + BLOCKTIME
        block_hash = hashlib.sha384()
        block_hash.update('{index}{prev_hash}{timestamp}'.format(index=self.index, prev_hash=self.prev_hash, timestamp=self.timestamp).encode('utf-8'))
        self.hash = str(block_hash.hexdigest())
        next_block_hash = hashlib.sha384()
        next_block_hash.update('{index}{prev_hash}{timestamp}'.format(index=self.index+1, prev_hash=self.hash, timestamp=self.next_timestamp).encode('utf-8'))
        self.next_hash = str(next_block_hash.hexdigest())

    '''
        * Format the block as json
    '''
    def finalize(self):
        return {
            'index':self.index,
            'timestamp':self.timestamp,
            'next_timestamp':self.next_timestamp,
            'block_hash':self.hash,
            'next_hash':self.next_hash,
            'prev_hash':self.prev_hash,
            'transfers':self.transfers
        }


    '''
        * Add a transfer object to the block
    '''
    def add_finalized_transfer(sender, recipient, amount, timestamp, public_key_pem, transaction_hash, signature):
        self.transfers.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount,
                'timestamp': timestamp,
                'public_key': public_key_pem,
                'transaction_hash': transaction_hash,
                'signature': signature
            }
        )

def tests():
    ''' Create empty Blocks
    chain = Blockchain()
    chain.teardown()
    for i in range(0, 3):
        block = Block()
        block.new(chain)
        chain.add_finalized_block(block.finalize())
    print(chain.chain)
    '''
    chain = Blockchain()
    chain.teardown()
    for i in range(0, 4):
        block = Block(None, None, None, None, None, None, [])
        block.new(chain)
        chain.add_finalized_block(block.finalize())
    print(chain.chain)
    chain = Blockchain()
    chain.update()
    print(chain.chain)
#tests()
