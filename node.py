from flask import Flask, request, jsonify
node = Flask(__name__)

@node.route('/', methods = ['GET'])
def DummyRoute():
    return '[]'

if __name__ == '__main__':
    node.run(threaded=True, host='localhost', port=8080, use_reloader=False)
