import requests, json
import time
import os, pickle
from chainspec import HOST, PORT, CHAIN_SYNC_INTERVAL, TEST_PEERS, RELATIVE_PATH
from core.blockchain import Blockchain, Block
from core.transfer import Transfer
'''
|----------------------------------------------------------|
|                    [Issues]
| 1. All Nodes need to sync the Txpool before creating
| a block.
| A transfer submitted at the time of block creation
| could corrupt the blockchain
|
|
|----------------------------------------------------------|

'''


class Core:
    def __init__(self, _Blockchain):
        self.blockchain = _Blockchain
    def next_block_timestamp(self):
        return self.blockchain.chain[-1]['next_timestamp']
    def last_block_timestamp(self):
        return self.blockchain.chain[-1]['timestamp']
    def height(self):
        return len(self.blockchain.chain)
    def create_next_block(self):
        prev_Block_Dict = self.blockchain.chain[-1]
        prev_Block = Block(prev_Block_Dict['index'], prev_Block_Dict['timestamp'], prev_Block_Dict['next_timestamp'], prev_Block_Dict['block_hash'], prev_Block_Dict['next_hash'], prev_Block_Dict['prev_hash'], prev_Block_Dict['transfers'])
        next_Block = Block(None, None, None, None, None, None, [])
        next_Block.new(prev_Block)
        self.blockchain.add_finalized_block(next_Block.finalize())
class ApiClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def get_blockchain(self, height):
        blockchain = requests.get('http://{host}:{port}/blockchain?height={height}'.format(host=self.host, port=self.port, height=height))
        return json.loads(blockchain.text)
    def get_height(self):
        height = requests.get('http://{host}:{port}/height'.format(host=self.host, port=self.port))
        return height.text
    def get_pool(self):
        pool = requests.get('http://{host}:{port}/txpool'.format(host=self.host, port=self.port))
        return json.loads(pool.text)


def reset(_Blockchain):
    # delete current chain datafile
    _Blockchain.teardown()
    # create new
    _Blockchain.new()
    genesis_Block = Block(None, None, None, None, None, None, [])
    genesis_Block.new(None)
    _Blockchain.add_finalized_block(genesis_Block.finalize())
def sync():
    instance = Blockchain()
    instance.update()
    c = Core(instance)
    while True:
        # make sure there is at least n peers online
        n = 1
        active = 0
        for PEER in TEST_PEERS:
            try:
                cli = ApiClient(PEER['HOST'], PEER['PORT'])
                cli.get_blockchain(c.height())
                active += 1
            except Exception as connerror:
                pass
        if active < n:
            print('[Error]: 0 peers online')
            time.sleep(5)
            continue

        # 1st check height of peers
        for PEER in TEST_PEERS:
            cli = ApiClient(PEER['HOST'], PEER['PORT'])
            #try:
            peer_height = int(cli.get_height())
            if peer_height > c.height():
                peer_chain = cli.get_blockchain(c.height())
                for block in peer_chain:
                    b = Block(block['index'], block['timestamp'], block['next_timestamp'], block['block_hash'], block['next_hash'], block['prev_hash'], block['transfers'])
                    for tx in b.transfers:
                        instance = Blockchain()
                        instance.update()
                        c = Core(instance)
                        if tx.validate(c) == False:
                            print('[Error]: Invalid transaction found in Block => Peer skipped: ', PEER)
                            time.sleep(600)
                    if c.blockchain.validate(b, False) == True:
                        print('[Info]: Block valid')
                        instance.add_finalized_block(b.finalize())
                    else:
                        print('[Error]: Block did not pass validaton => Peer skipped: ', PEER)
                        continue
            else:
                print('[Info]: Nothing to sync')
            #except Exception as connerr:
            #    print(connerr)
            #    print('[Warning]: Connection lost: ', PEER)
        print('[Info]: Done! @', str(time.time()))

        # before block creation, sync the txpool with all peers
        for PEER in TEST_PEERS:
            local_pool = []
            cli = ApiClient(PEER['HOST'], PEER['PORT'])
            if not os.path.exists(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=c.height())):
                pass
            else:
                with open(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=c.height()), 'rb') as pool_file:
                    local_pool = pickle.load(pool_file)
            # sync and add to pool
            #try:
            peer_height = int(cli.get_height())
            if peer_height == c.height():
                peer_pool = cli.get_pool()
                print("[Info]: Peer Pool -> ", peer_pool)
                for tx in peer_pool:
                    if not tx in local_pool:
                        instance = Blockchain()
                        instance.update()
                        c = Core(instance)
                        _tx = Transfer(tx['sender'], tx['recipient'], tx['amount'], tx['timestamp'], tx['transaction_hash'], tx['signature'], tx['public_key'], None, None)
                        # TBD: revert if invalid, add balance checks
                        print("[Info]: Tx valid -> ", _tx.validate(c))
                        _tx.finalize()
                        _tx.add_to_pool(c.height())
                        print("[Success]: Tx synced!")
            #except Exception as connerr:
            #    print(connerr)
            #    print('[Warning]: Connection lost: ', PEER)

        # create a new block if it is time
        if c.next_block_timestamp() <= time.time():
            c.create_next_block()
            print('[Success]: Block created -> ', c.height())

        '''

        blockchain = get_blockchain_from_peer(HOST, PORT)
        print(blockchain)


        '''




        time.sleep(CHAIN_SYNC_INTERVAL)


'''

Transaction takes effect on Balance after n block confirmations.
Issue:
    Front-running is possible and can potentially cause a chainsplit

'''
