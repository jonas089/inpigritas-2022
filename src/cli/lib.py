import sys
import os
import requests
import json
module_path = os.path.abspath('../src')
sys.path.insert(0, module_path)

'''
    Api client to send requests to nodes
'''
class ApiClient:

    '''
        Initialise a new client instance
        :param host: Ip address to bind http server
        :type host: str
        :param port: Port to bind http server
        :type port: int
    '''
    def __init__(self, host, port):
        self.host = host
        self.port = port

    '''
        Get the blockchain from a node
        :param height: Query blockchain from height onwards (inclusive)
        :return: Json dump of a blockchain
        :rtype: json
    '''
    def get_blockchain(self, height):
        blockchain = requests.get('http://{host}:{port}/read/blockchain?height={height}'.format(host=self.host, port=self.port, height=height))
        return json.loads(blockchain.text)

    '''
        Get the current transaction pool from a node
        :return: Transaction pool for current block
        :rtype: json
    '''
    def get_pool(self):
        pool = requests.get('http://{host}:{port}/read/txpool'.format(host=self.host, port=self.port))
        return json.loads(pool.text)

    '''
        Get the current height of a node
        :return: Current node height
        :rtype: str
    '''
    def get_height(self):
        height = requests.get('http://{host}:{port}/status/height'.format(host=self.host, port=self.port))
        return height.text
