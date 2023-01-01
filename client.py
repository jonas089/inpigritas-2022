import requests, json
import time
from chainspec import HOST, PORT, CHAIN_SYNC_INTERVAL
from core.blockchain import Blockchain, Block
class Core:
    def __init__(self, _Blockchain):
        self.blockchain = _Blockchain
    def next_block_timestamp(self):
        return self.blockchain.chain[-1]['next_timestamp']
    def create_next_block(self):
        prev_Block_Dict = self.blockchain.chain[-1]
        prev_Block = Block(prev_Block_Dict['index'], prev_Block_Dict['timestamp'], prev_Block_Dict['next_timestamp'], prev_Block_Dict['block_hash'], prev_Block_Dict['next_hash'], prev_Block_Dict['prev_hash'], prev_Block_Dict['transfers'])
        next_Block = Block(None, None, None, None, None, None, [])
        next_Block.new(prev_Block)
        self.blockchain.add_finalized_block(next_Block.finalize())
class ApiClient:
    def __init__(self, host, port):
        self.host = host,
        self.port = port
    def get_blockchain_from_peer(self):
        blockchain = requests.get('http://{host}:{port}/blockchain'.format(host=self.host, port=self.port))
        return json.loads(blockchain.text)
    def get_height_from_peer(self):
        height = requests.get('http://{host}:{port}/height'.format(host=self.host, port=self.port))
        return height.text
    def get_tx_pool_from_peer(self):
        pool = requests.get('http://{host}:{port}/txpool'.format(host=self.host, port=self.port))
        return json.loads(pool.text)
def reset(_Blockchain):
    # delete current chain datafile
    _Blockchain.teardown()
    # create new
    _Blockchain.new()
    genesis_Block = Block(None, None, None, None, None, None, [])
    genesis_Block.new(None)
    _Blockchain.add_finalized_block(genesis_Block)
def sync():
    instance = Blockchain()
    instance.update()
    c = Core(instance)
    cli = ApiClient('localhost', 8080)
    while True:
        # 1st check height of peers
        # if height match, sync txpool
        # if height && timestamp match, create block
        # otherwise sync blocks

        # Test local Block creation
        #print(c.next_block_timestamp())
        #print(c.blockchain.chain)
        if c.next_block_timestamp() <= time.time():
            c.create_next_block()
        print(c.blockchain.chain)
        '''

        blockchain = get_blockchain_from_peer(HOST, PORT)
        print(blockchain)


        '''




        time.sleep(CHAIN_SYNC_INTERVAL)
