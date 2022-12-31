from flask import Flask, request, jsonify
from chainspec import HOST, PORT
import os, pickle
api = Flask(__name__)
def get_local_height():
    with open('./data/blockchain.dat', 'rb') as chain_file:
        print('[API] Incoming Request from peer: ', request.remote_addr)
        blockchain = pickle.load(chain_file)
        current_height = blockchain[-1]['index'] + 1
        return current_height
@api.route('/', methods=['GET'])
def InpigritasApi():
    return '''
    Inpigritas
    '''
@api.route('/blockchain', methods=['GET'])
def Blockchain():
    with open('./data/blockchain.dat', 'rb') as chain_file:
        print('[API] Incoming Request from peer: ', request.remote_addr)
        return pickle.load(chain_file)
@api.route('/height', methods=['GET'])
def height():
    return str(get_local_height())
@api.route('/txpool', methods=['GET'])
def txpool():
    height = get_local_height()
    if not os.path.exists('./txpool/{height}.dat'.format(height=height)):
        return '[]'
    with open('./txpool/{height}.dat'.format(height=height)) as pool_file:
        return pickle.load(pool_file)
def main():
    api.run(threaded=True, host=HOST, port=PORT)
