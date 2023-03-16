from flask import Flask, request, jsonify
from chainspec import HOST, PORT, RELATIVE_PATH, CONFIRMATIONS, TEST_PEERS
import os, pickle, json
from core.blockchain import Blockchain
from core.transfer import Transfer
from client import is_synced

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
    if not is_synced(instance, TEST_PEERS):
        return "[Error] tx: Node needs to sync first!"
    # Warning: currently only checking for duplicates in current pool
    tx = request.json
    if instance.is_duplicate_in_pool(tx):
        return "[Error] tx: Transaction is a duplicate!"
    tx_obj = Transfer(tx['sender'], tx['recipient'], tx['amount'], tx['timestamp'], tx['transaction_hash'], tx['signature'], tx['public_key'], None, None)
    tx_obj.add_to_pool(instance.height()+CONFIRMATIONS)
    return "[Success] tx: accepted!"


# Chain info
@api.route('/status/height', methods=['GET'])
def StatusHeight():
    instance = Blockchain()
    return str(instance.height())

# export
def main():
    api.run(threaded=True, host=HOST, port=PORT)
