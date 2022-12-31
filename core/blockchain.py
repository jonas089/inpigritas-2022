import os, time, hashlib, pickle, base64
import chainspec
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA384
class Blockchain():
    def __init__(self):
        self.chain = []
    def new(self):
        if not os.path.exists('./data/blockchain.dat'):
            open('./data/blockchain.dat', 'x')
        else:
            os.remove('./data/blockchain.dat')
            open('./data/blockchain.dat', 'x')
    def update(self):
        try:
            with open('./data/blockchain.dat', 'rb') as chain_file:
                self.chain = pickle.load(chain_file)
        except Exception as empty:
            self.chain = []
    def write(self):
        with open('./data/blockchain.dat', 'wb') as chain_file:
            pickle.dump(self.chain, chain_file)
        self.update()
    def add_finalized_block(self, Block):
        # Read txpool for current Block and append transactions
        if os.path.exists('./txpool/{index}.dat'.format(index=Block['index'])):
            with open('./txpool/{index}.dat'.format(index=Block['index']), 'rb') as pool_file:
                Block['transfers'] = [*Block['transfers'], *pickle.load(pool_file)]
                os.remove('./txpool/{index}.dat'.format(index=Block['index']))
        self.chain.append(Block)
        self.write()
    def teardown(self):
        os.remove('./data/blockchain.dat')
    def validate(self, Block):
        # Block can not be in the future
        if Block.timestamp > time.time():
            return False
        prev_Block_Dict = blockchain[Block.index - 1]
        prev_Block = Block(prev_Block_Dict['index'], prev_Block_Dict['timestamp'], prev_Block_Dict['next_timestamp'], prev_Block_Dict['block_hash'], prev_Block_Dict['next_hash'], prev_Block_Dict['prev_hash'], prev_Block_Dict['transfers'])
        # compare Blocks
        if prev_Block.hash != Block.prev_hash or prev_Block.next_hash != Block.hash or prev_Block.index != (Block.index - 1) or prev_Block.next_timestamp != Block.timestamp:
            return False
        # validate Block hash
        block_hash = hashlib.sha384()
        block_hash.update('{index}{prev_hash}{timestamp}'.format(index=Block.index, prev_hash=Block.prev_hash, timestamp=Block.timestamp).encode('utf-8'))
        _hash = str(block_hash.hexdigest())
        if block_hash != Block.hash or block_hash != prev_Block.next_block_hash:
            return False
        # validate Transfers in Block using Transfer class

        return True
class Block():
    def __init__(self, index, timestamp, next_timestamp, block_hash, next_hash, prev_hash, transfers):
        self.index = index
        self.timestamp = timestamp
        self.next_timestamp = next_timestamp
        self.hash = block_hash
        self.next_hash = next_hash
        self.prev_hash = prev_hash
        self.transfers = transfers
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
                    'recipient':chainspec.ACCOUNT,
                    'amount':chainspec.PREMINE,
                    'timestamp': time.time()
                }
            )
            self.timestamp = time.time()
        self.next_timestamp = self.timestamp + chainspec.BLOCKTIME
        block_hash = hashlib.sha384()
        block_hash.update('{index}{prev_hash}{timestamp}'.format(index=self.index, prev_hash=self.prev_hash, timestamp=self.timestamp).encode('utf-8'))
        self.hash = str(block_hash.hexdigest())
        next_block_hash = hashlib.sha384()
        next_block_hash.update('{index}{prev_hash}{timestamp}'.format(index=self.index+1, prev_hash=self.hash, timestamp=self.next_timestamp).encode('utf-8'))
        self.next_hash = str(next_block_hash.hexdigest())
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
