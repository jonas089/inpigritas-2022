import os, time, hashlib, pickle, base64
from chainspec import ACCOUNT, PREMINE, BLOCKTIME, RELATIVE_PATH
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA384

'''
    Prototype Blockchain class and 'database'
'''
class Blockchain():

    '''
        Initialise a new Blockchain or import an existing Blockchain
        :return: ()
        :rtype: ()
    '''
    def __init__(self):
        self.chain = []
        self.update()

    '''
        Create a new blockchain data file and clear a potentially existing blockchain
        :return: ()
        :rtype: ()
    '''
    def new(self):
        if not os.path.exists(RELATIVE_PATH + '/data/blockchain.dat'):
            open(RELATIVE_PATH + '/data/blockchain.dat', 'x')
        else:
            os.remove(RELATIVE_PATH + '/data/blockchain.dat')
            open(RELATIVE_PATH + '/data/blockchain.dat', 'x')

    '''
        Update the instance by reading from the existing blockchain file
        :return: ()
        :rtype: ()
    '''
    def update(self):
        try:
            with open(RELATIVE_PATH + '/data/blockchain.dat', 'rb') as chain_file:
                self.chain = pickle.load(chain_file)
        except Exception as empty:
            self.chain = []

    '''
        Read from the blockchain file
        :return: Blockchain dump
        :rtype: json
    '''
    def read(self):
        with open(RELATIVE_PATH + '/data/blockchain.dat', 'rb') as chain_file:
            return pickle.load(chain_file)

    '''
        Write to the blockchain file
        :return: ()
        :rtype: ()
    '''
    def write(self):
        with open(RELATIVE_PATH + '/data/blockchain.dat', 'wb') as chain_file:
            pickle.dump(self.chain, chain_file)
        self.update()

    '''
        Delete the existing blockchain file
        :return: ()
        :rtype: ()
    '''
    def teardown(self):
        if os.path.exists(RELATIVE_PATH + '/data/blockchain.dat'):
            os.remove(RELATIVE_PATH + '/data/blockchain.dat')

    '''
        Add a block to the chain
        :param: block
        :type block: finalized Block
        :return: ()
        :rtype: ()
    '''
    def add_finalized_block(self, block):
        # Read txpool for current Block and append transactions
        if os.path.exists(RELATIVE_PATH + '/txpool/{index}.dat'.format(index=block['index'])):
            with open(RELATIVE_PATH + '/txpool/{index}.dat'.format(index=block['index']), 'rb') as pool_file:
                try:
                    block['transfers'] = [*block['transfers'], *pickle.load(pool_file)]
                except Exception as Empty:
                    block['transfers'] = [*block['transfers'], *[]]
                os.remove(RELATIVE_PATH + '/txpool/{index}.dat'.format(index=block['index']))
        self.chain.append(block)
        self.write()

    '''
        Add an external block to the chain that was received from a peer
        :param: block
        :type block: finalized Block
        :return: ()
        :rtype: ()
    '''
    def add_external_finalized_block(self, block):
        self.chain.append(block)
        self.write()
        if os.path.exists(RELATIVE_PATH + '/txpool/{index}.dat'.format(index=block['index'])):
            os.remove(RELATIVE_PATH + '/txpool/{index}.dat'.format(index=block['index']))

    '''
        Validate a block
        :param: block
        :type block: Block
        :param: allow_future_blocks
        :type allow_future_blocks: bool
        :return: Validation result
        :rtype: bool
    '''
    def validate(self, block, allow_future_blocks):
        # Block can not be in the future
        if block.timestamp > time.time() and allow_future_blocks == False:
            return False
        prev_block_dict = self.chain[block.index - 1]
        prev_block = Block(prev_block_dict['index'], prev_block_dict['timestamp'], prev_block_dict['next_timestamp'], prev_block_dict['block_hash'], prev_block_dict['next_hash'], prev_block_dict['prev_hash'], prev_block_dict['transfers'])
        # compare Blocks
        if prev_block.hash != block.prev_hash or prev_block.next_hash != block.hash or prev_block.index != (block.index - 1) or prev_block.next_timestamp != block.timestamp:
            return False
        # validate Block hash
        block_hash = hashlib.sha384()
        block_hash.update('{index}{prev_hash}{timestamp}'.format(index=block.index, prev_hash=block.prev_hash, timestamp=block.timestamp).encode('utf-8'))
        _hash = str(block_hash.hexdigest())
        if _hash != block.hash or _hash != prev_block.next_hash:
            return False
        # validate Transfers in Block using Transfer class
        return True

    '''
        Get the height of the local blockchain
        :return: Chain height
        :rtype: int
    '''
    def height(self):
        return len(self.chain) + 1

    '''
        Get the timestamp of the next block
        :return: Next block timetsamp
        :rtype: int
    '''
    def next_block_timestamp(self):
        return self.chain[-1]['next_timestamp']

    '''
        Get the timestamp of the next block
        :return: Next block timetsamp
        :rtype: int
    '''
    def last_block_timestamp(self):
        return self.chain[-1]['timestamp']

    '''
        Create a new block based on consensus
        :return: ()
        :rtype: ()
    '''
    def create_next_block(self):
        prev_block_dict = self.chain[-1]
        prev_block = Block(prev_block_dict['index'], prev_block_dict['timestamp'], prev_block_dict['next_timestamp'], prev_block_dict['block_hash'], prev_block_dict['next_hash'], prev_block_dict['prev_hash'], prev_block_dict['transfers'])
        next_Block = Block(None, None, None, None, None, None, [])
        next_Block.new(prev_block)
        self.add_finalized_block(next_Block.finalize())

    '''
        Get the local transaction pool for the current block
        :return: Transaction pool for current block
        :rtype: json
    '''
    def txpool(self):
        if not os.path.exists(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=self.height())):
            return []
        else:
            with open(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=self.height()), 'rb') as pool_file:
                return pickle.load(pool_file)

    '''
        Check for a duplicate transaction or resumbission in the currently active transaction pool
        :param: tx
        :type tx: finalized Transaction
        :return: Duplicate-check result
        :rtype: bool
    '''
    def is_duplicate_in_pool(self, tx):
        local_pool = self.txpool()
        if len(local_pool) != 0:
            for _tx in local_pool:
                if tx['transaction_hash'] == _tx['transaction_hash']:
                    return True
        return False

'''
    Block as an object with attributes and methods
'''
class Block():

    '''
        Initialise a new Block from parameters
        :param: index
        :type index: int
        :param: timestamp
        :type timestamp: str
        :param: next_timestamp
        :type next_timestamp: str
        :param: block_hash
        :type block_hash: str
        :param: next_hash
        :type next_hash: str
        :param: prev_hash
        :type prev_hash: str
        :param: transfers
        :type transfer: dict
        :return: ()
        :rtype: ()
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
        Create a new block with timestamp and hash
        :param: prev_block
        :type prev_block: Block
        :return: ()
        :rtype: ()
    '''
    def new(self, prev_block):
        if prev_block == None:
            self.index = 0
        else:
            self.index = prev_block.index + 1
        if self.index != 0:
            self.prev_hash = prev_block.hash
            self.timestamp = prev_block.next_timestamp
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
        Represent the block as json
        :return: finalized Block
        :rtype: json
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
