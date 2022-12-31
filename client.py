import requests, json
import time

from chainspec import HOST, PORT, CHAIN_SYNC_INTERVAL
def get_blockchain_from_peer(host, port):
    blockchain = requests.get('http://{host}:{port}/blockchain'.format(host=host, port=port))
    return json.loads(blockchain.text)
def get_height_from_peer(host, port):
    height = requests.get('http://{host}:{port}/height'.format(host=host, port=port))
    return height.text
def get_tx_pool_from_peer(host, port):
    pool = requests.get('http://{host}:{port}/txpool'.format(host=host, port=port))
    return json.loads(pool.text)
def sync():
    while True:
        pool = get_tx_pool_from_peer(HOST, PORT)
        print(pool)
        time.sleep(CHAIN_SYNC_INTERVAL)
