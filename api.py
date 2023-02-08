from flask import Flask, request, jsonify
from chainspec import HOST, PORT
import os, pickle
from core.blockchain import Blockchain
api = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@api.route('/', methods=['GET'])
def InpigritasApi():
    return '''
    Inpigritas
    '''
@api.route('/blockchain', methods=['GET'])
def block_chain():
    index = int(request.args.get('height'))
    b = Blockchain()
    b.update()
    return b.chain[index:]
@api.route('/height', methods=['GET'])
def get_local_height():
    b = Blockchain()
    b.update()
    return str(len(b.chain))
@api.route('/txpool', methods=['GET'])
def txpool():
    height = get_local_height()
    if not os.path.exists('./txpool/{height}.dat'.format(height=height)):
        return '[]'
    with open('./txpool/{height}.dat'.format(height=height), 'rb') as pool_file:
        try:
            return pickle.load(pool_file)
        except Exception as Empty:
            return []
def main():
    api.run(threaded=True, host=HOST, port=PORT)
