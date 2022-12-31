from flask import Flask, request, jsonify
from chainspec import HOST, PORT
import os, pickle
from core.blockchain import Blockchain
api = Flask(__name__)
@api.route('/', methods=['GET'])
def InpigritasApi():
    return '''
    Inpigritas
    '''
@api.route('/blockchain', methods=['GET'])
def block_chain():
    b = Blockchain()
    b.update()
    return b.chain
@api.route('/height', methods=['GET'])
def height():
    b = Blockchain()
    b.update()
    return str(len(b.chain))
@api.route('/txpool', methods=['GET'])
def txpool():
    height = get_local_height()
    if not os.path.exists('./txpool/{height}.dat'.format(height=height)):
        return '[]'
    with open('./txpool/{height}.dat'.format(height=height)) as pool_file:
        return pickle.load(pool_file)
def main():
    api.run(threaded=True, host=HOST, port=PORT)
