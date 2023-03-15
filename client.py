import requests, json
import time
import os, pickle
from chainspec import HOST, PORT, CHAIN_SYNC_INTERVAL, TEST_PEERS, RELATIVE_PATH
from core.blockchain import Blockchain, Block
from core.transfer import Transfer

# This is to be moved
class ApiClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    def get_blockchain(self, height):
        blockchain = requests.get('http://{host}:{port}/read/blockchain?height={height}'.format(host=self.host, port=self.port, height=height))
        return json.loads(blockchain.text)
    def get_pool(self):
        pool = requests.get('http://{host}:{port}/read/txpool'.format(host=self.host, port=self.port))
        return json.loads(pool.text)
    def get_height(self):
        height = requests.get('http://{host}:{port}/status/height'.format(host=self.host, port=self.port))
        return height.text

# Synchronization loop and Consensus
def sync():
    start_time = time.time()
    instance = Blockchain()
    while True:
        # Look for active peers
        n = 1
        active = 0
        for PEER in TEST_PEERS:
            try:
                cli = ApiClient(PEER['HOST'], PEER['PORT'])
                cli.get_blockchain(instance.height())
                active += 1
            except Exception as connerror:
                pass
        if active < n:
            print('[Error]: 0 peers online, trying again in 60 seconds!')
            time.sleep(60)
            continue

        # Sync Blocks with active peers ( subject to a majority threshold )
        for PEER in TEST_PEERS:
            cli = ApiClient(PEER['HOST'], PEER['PORT'])
            try:
                peer_height = int(cli.get_height())
                if peer_height > instance.height():
                    peer_chain = cli.get_blockchain(instance.height())
                    for block in peer_chain:
                        b = Block(block['index'], block['timestamp'], block['next_timestamp'], block['block_hash'], block['next_hash'], block['prev_hash'], block['transfers'])
                        for tx in b.transfers:
                            instance.update()
                            _tx = Transfer(tx['sender'], tx['recipient'], tx['amount'], tx['timestamp'], tx['transaction_hash'], tx['signature'], tx['public_key'], None, None)
                            if _tx.validate(c) == False:
                                print('[Error]: Invalid transaction found in Block => Peer skipped: ', PEER)
                                time.sleep(600)
                        if instance.validate(b, False) == True:
                            print('[Info]: Block valid')
                            instance.add_external_finalized_block(b.finalize())
                        else:
                            print('[Error]: Block did not pass validaton => Peer skipped: ', PEER)
                            continue
                else:
                    print('[Info]: Nothing to sync')
            except Exception as connerr:
                print(connerr)
                print('[Warning]: Connection lost: ', PEER)
        print('[Info]: Done! @', str(time.time()))

        # Sync Transactions with active peers ( subject to a majority threshold )
        for PEER in TEST_PEERS:
            local_pool = []
            cli = ApiClient(PEER['HOST'], PEER['PORT'])
            if not os.path.exists(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=instance.height())):
                pass
            else:
                with open(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=instance.height()), 'rb') as pool_file:
                    local_pool = pickle.load(pool_file)
            try:
                peer_height = int(cli.get_height())
                if peer_height == instance.height():
                    peer_pool = cli.get_pool()
                    for tx in peer_pool:
                        # check tx hash instead
                        is_duplicate = False
                        if len(local_pool) != 0:
                            for __tx in local_pool:
                                if __tx['transaction_hash'] == tx['transaction_hash']:
                                    is_duplicate = True

                        if is_duplicate == False:
                            instance.update()
                            _tx = Transfer(tx['sender'], tx['recipient'], tx['amount'], tx['timestamp'], tx['transaction_hash'], tx['signature'], tx['public_key'], None, None)
                            # TBD: revert if invalid, add balance checks
                            print("[Info]: Tx valid -> ", _tx.validate(instance))
                            _tx.add_to_pool(instance.height())
                            print("[Success]: Tx synced!")
            except Exception as connerr:
                print(connerr)
                print('[Warning]: Connection lost: ', PEER)

        # Create a new Block
        if instance.next_block_timestamp() <= time.time():
            instance.create_next_block()
            print('[Success]: Block created -> ', str(instance.height() - 1))

        # Await next sync period
        print('Runtime: ', str(time.time() - start_time)[:-5])
        time.sleep(CHAIN_SYNC_INTERVAL)


'''

Transaction takes effect on Balance after n block confirmations.
Issue:
    Front-running is possible and can potentially cause a chainsplit

'''
