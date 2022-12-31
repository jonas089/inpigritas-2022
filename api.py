from flask import Flask, request, jsonify
from chainspec import HOST, PORT
import pickle
api = Flask(__name__)

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
    with open('./data/blockchain.dat', 'rb') as chain_file:
        print('[API] Incoming Request from peer: ', request.remote_addr)
        blockchain = pickle.load(chain_file)
        current_height = blockchain[-1]['index'] + 1
        return str(current_height)
def main():
    api.run(threaded=True, host=HOST, port=PORT)
