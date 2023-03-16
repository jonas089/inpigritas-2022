import requests, json
import time
import os, pickle
from chainspec import HOST, PORT, CHAIN_SYNC_INTERVAL, TEST_PEERS, RELATIVE_PATH
from core.blockchain import Blockchain, Block
from core.transfer import Transfer

'''
    TBD: introduce error types
    split sync_blocks and sync_transactions up in specialized functions

'''


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

def is_synced(instance, peers):
    for peer in peers:
        cli = ApiClient(peer['HOST'], peer['PORT'])
        try:
            peer_height = int(cli.get_height())
            if peer_height > instance.height():
                return False
        except Exception as connerr:
            print(connerr)
            print('[Warning]: Connection lost: ', peer)
    return True

def sync_blocks(instance, peers):
    for peer in peers:
        cli = ApiClient(peer['HOST'], peer['PORT'])
        try:
            peer_height = int(cli.get_height())
            if peer_height > instance.height():
                peer_chain = cli.get_blockchain(instance.height())
                for block in peer_chain:
                    b = Block(block['index'], block['timestamp'], block['next_timestamp'], block['block_hash'], block['next_hash'], block['prev_hash'], block['transfers'])
                    for tx in b.transfers:
                        instance.update()
                        tx_obj = Transfer(tx['sender'], tx['recipient'], tx['amount'], tx['timestamp'], tx['transaction_hash'], tx['signature'], tx['public_key'], None, None)
                        if tx_obj.validate(c) == False:
                            print('[Error]: Invalid transaction found in Block => Peer skipped: ', peer)
                            time.sleep(600)
                                            #False: don't allow blocks that are in the future.
                    if instance.validate(b, False) == True:
                        print('[Info]: Block valid')
                        instance.add_external_finalized_block(b.finalize())
                    else:
                        print('[Error]: Block did not pass validaton => Peer skipped: ', peer)
                        continue
            else:
                print('[Info]: Nothing to sync')
        except Exception as connerr:
            print(connerr)
            print('[Warning]: Connection lost: ', peer)

def sync_transactions(instance, peers):
    for peer in peers:
        cli = ApiClient(peer['HOST'], peer['PORT'])
        local_pool = instance.txpool()
        # remove
        _h = instance.height()
        print("Pool:{pl}, height:{ht}".format(pl=str(local_pool), ht=str(_h)))
        # until here
        try:
            peer_height = int(cli.get_height())
            if peer_height == instance.height():
                peer_pool = cli.get_pool()
                for tx in peer_pool:
                    if len(local_pool) != 0 and len(peer_pool) > len(local_pool):
                        if not instance.is_duplicate_in_pool(tx):
                            instance.update()
                            tx_obj = Transfer(tx['sender'], tx['recipient'], tx['amount'], tx['timestamp'], tx['transaction_hash'], tx['signature'], tx['public_key'], None, None)
                            print("[Info]: Tx valid -> ", tx_obj.validate(instance))
                            #tx_obj.add_to_pool(instance.height())
                            print("[Success]: Tx synced!")
                    elif len(local_pool) == 0 and len(peer_pool) == 0:
                        print("[Info]: no transaction found.")
                    else:
                        print("[Info]: Local pool: {lp} transactions Peer pool: {pp} transactions".format(lp=str(len(local_pool)), pp=str(len(peer_pool))))
        except Exception as connerr:
            print('[Warning]: Connection lost: ', PEER)
            print("[Error]: ", connerr)
# Synchronization loop and Consensus
def sync():
    start_time = time.time()
    instance = Blockchain()
    while True:
        # Look for active peers - temporary solution
        n = 1
        active = 0
        for peer in TEST_PEERS:
            try:
                cli = ApiClient(peer['HOST'], peer['PORT'])
                cli.get_blockchain(instance.height())
                active += 1
            except Exception as connerror:
                print(connerror)
                pass
        if active < n:
            print('[Error]: 0 peers online, trying again in 60 seconds!')
            time.sleep(60)
            continue
        #################################################################

        # Sync Blocks with active peers ( subject to a majority threshold )
        sync_blocks(instance, TEST_PEERS)
        sync_transactions(instance, TEST_PEERS)
        print('[Info]: Sync Done! @', str(time.time()))
        # Create a new Block
        if instance.next_block_timestamp() <= time.time():
            instance.create_next_block()
            print('[Success]: Block created -> ', str(instance.height() - 1))

        # Await next sync period
        print('Runtime: ', str(time.time() - start_time)[:-5])
        time.sleep(CHAIN_SYNC_INTERVAL)
