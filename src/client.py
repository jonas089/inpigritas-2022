import requests, json
import time
import os, pickle
from chainspec import HOST, PORT, CHAIN_SYNC_INTERVAL, TEST_PEERS, RELATIVE_PATH
from core.blockchain import Blockchain, Block
from core.transfer import Transfer
from sync.blk import sync_proto as blk_sync_proto
from sync.tx import sync_proto as tx_sync_proto
from sync.lib import is_synced as is_sync_proto
from cli.lib import ApiClient
'''
    TBD: introduce error types
    split sync_blocks and sync_transactions up in specialized functions

'''

def sync_blocks(instance, peers):
    blk_sync_proto(instance, peers)

def sync_transactions(instance, peers):
    tx_sync_proto(instance, peers)

def is_synced(instance, peers):
    return is_sync_proto(instance, peers)

'''Network synchronisation loop
    * check amount of active peers
    * at least one peer must be active
'''
def sync():
    start_time = time.time()
    instance = Blockchain()
    while True:
        '''
            * check amount of active peers
            * at least one peer must be active
        '''
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

        '''
            * sync blocks
            * sync transactions in the currently selected pool
        '''
        sync_blocks(instance, TEST_PEERS)
        sync_transactions(instance, TEST_PEERS)
        print('[Info]: Sync Done! @', str(time.time()))
        '''
            * create a new block if fully synced
            * small blocktime can cause disorder in prototype
        '''
        if is_synced() and instance.next_block_timestamp() <= time.time():
            instance.create_next_block()
            print('[Success]: Block created -> ', str(instance.height() - 1))

        '''
            * await the next synchronization round and repeat
        '''
        print('Runtime: ', str(time.time() - start_time)[:-5])
        time.sleep(CHAIN_SYNC_INTERVAL)
