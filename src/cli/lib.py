import sys
import os
import requests
import json
module_path = os.path.abspath('../src')
sys.path.insert(0, module_path)

'''
    * Api client to get from the http server
'''
class ApiClient:

    '''
        * Initialise the client by setting a peer
        * The docker image handles this
    '''
    def __init__(self, host, port):
        self.host = host
        self.port = port

    '''
        * read the blockchain json dump from a peer
    '''
    def get_blockchain(self, height):
        blockchain = requests.get('http://{host}:{port}/read/blockchain?height={height}'.format(host=self.host, port=self.port, height=height))
        return json.loads(blockchain.text)

    '''
        * read the active transaction pool from a peer
    '''
    def get_pool(self):
        pool = requests.get('http://{host}:{port}/read/txpool'.format(host=self.host, port=self.port))
        return json.loads(pool.text)

    '''
        * get the next blocks height from a peer
    '''
    def get_height(self):
        height = requests.get('http://{host}:{port}/status/height'.format(host=self.host, port=self.port))
        return height.text
