from flask import Flask, request, jsonify
from chainspec import HOST, PORT, RELATIVE_PATH
import os, pickle
from core.blockchain import Blockchain
api = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Web
@api.route('/', methods=['GET'])
def InpigritasApi():
    return "Inpigritas"

# Consensus data
@api.route('/read/blockchain', methods=['GET'])
def GetBlockChain():
    index = int(request.args.get('height'))
    b = Blockchain()
    return b.chain[index:]

@api.route('/read/txpool', methods=['GET'])
def GetTxPool():
    height = StatusHeight()
    if not os.path.exists(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=height)):
        return '[]'
    with open(RELATIVE_PATH + '/txpool/{height}.dat'.format(height=height), 'rb') as pool_file:
        try:
            return pickle.load(pool_file)
        except Exception as Empty:
            return []

# Consensus post
@api.route('/propose/tx', methods=['POST'])
def ProposeTx():
    tx = request.form.get('tx')


# Chain info
@api.route('/status/height', methods=['GET'])
def StatusHeight():
    b = Blockchain()
    return str(b.height())

# export
def main():
    api.run(threaded=True, host=HOST, port=PORT)
