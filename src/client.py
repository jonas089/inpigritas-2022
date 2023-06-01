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
    Inpigritas node client
    :param: peers
    :type peers: str[]
'''

def connect(peers):
    active = 0
    for peer in peers:
        try:
            cli = ApiClient(peer['HOST'], peer['PORT'])
            cli.get_height()
            active += 1
        except Exception as connerror:
            print(connerror)
            pass
    return active

'''
    Sync Blocks call
    :param: instance
    :type instance: Blockchain
'''
def sync_blocks(instance, peers):
    blk_sync_proto(instance, peers)

'''
    Sync Transactions call
    :param: instance
    :type instance: Blockchain
'''
def sync_transactions(instance, peers):
    tx_sync_proto(instance, peers)

'''
    Check if synced with peers
    :param: instance
    :type instance: Blockchain
    :param: peers
    :type peers: str[]
    :return: Result
    :rtype: bool
'''
def is_synced(instance, peers):
    return is_sync_proto(instance, peers)

'''
    Create new block event
    :param: instance
    :type instance: Blockchain
'''
def new_block(instance):
    if is_synced(instance, TEST_PEERS) and instance.next_block_timestamp() <= time.time():
        instance.create_next_block()
        print('[Success]: Block created -> ', str(instance.height() - 1))

'''
    Network synchronisation loop
'''
def sync():
    start_time = time.time()
    instance = Blockchain()
    while True:
        active = connect(TEST_PEERS)
        n=1
        if active < n:
            print('[Error]: 0 peers online, trying again in 60 seconds!')
            time.sleep(60)
            continue

        sync_blocks(instance, TEST_PEERS)
        sync_transactions(instance, TEST_PEERS)
        print('[Info]: Sync Done! @', str(time.time()))

        new_block(instance)

        print('Runtime: ', str(time.time() - start_time)[:-5])
        time.sleep(CHAIN_SYNC_INTERVAL)
