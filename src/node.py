from flask import Flask, request, jsonify
from config import HOST, PORT, RELATIVE_PATH, CONFIRMATIONS, TEST_PEERS, PATH_TO_DB
from core.blockchain import BlockChain
from core.factory import BlockFactory

node = Flask(__name__)

@node.route('/', methods=['GET'])
def Ping():
    return HOST

@node.route('/docs', methods=['GET'])
def Documentation():
    return "TBD: Create docs."

@node.route('/status/height', methods=['GET'])
def StatusHeight():
    blockchain = BlockChain(PATH_TO_DB)
    serialized_block = blockchain.get_last_block().serialize()
    return serialized_block

def start():
    node.run(threaded=True, host=HOST, port=PORT, debug=True)