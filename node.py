import requests, json
import time
def Blockchain():
    blockchain = requests.get('http://127.0.0.1:8080/blockchain')
    print(blockchain)

def sync():
    while True:
        print('Sync process: alive')
        time.sleep(5)
