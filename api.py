from flask import Flask, request, jsonify
import pickle
node = Flask(__name__)

@node.route('/blockchain', methods=['GET'])
def Blockchain():
    with open('./data/blockchain.dat', 'rb') as blockchain:
        return pickle.load(blockchain)

def main():
    node.run(threaded=True, host='localhost', port=8080, use_reloader=False)
