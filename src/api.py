from flask import Flask, request, jsonify
from chainspec import HOST, PORT, RELATIVE_PATH, CONFIRMATIONS
import os, pickle
from core.blockchain import Blockchain
from core.transfer import Transfer
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
    instance = Blockchain()
    return instance.chain[index:]

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
    instance = Blockchain()
    tx = request.form.get('tx')
    # missing: validate transaction - check for duplicates & sig.verify
    # need to find a way to prevent nodes from changing tx height / mature the tx once submitted. 
    tx_obj = Transfer(tx['sender'], tx['recipient'], tx['amount'], tx['timestamp'], tx['transaction_hash'], tx['signature'], tx['public_key'], None, None)
    tx_obj.add_to_pool(instance.height()+CONFIRMATIONS)



# Chain info
@api.route('/status/height', methods=['GET'])
def StatusHeight():
    instance = Blockchain()
    return str(instance.height())

# export
def main():
    api.run(threaded=True, host=HOST, port=PORT)
