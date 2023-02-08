import os
BLOCKTIME = 60 # 3 minutes
ACCOUNT = '0x00' # premine address
PREMINE = 1_000_000
HOST = 'localhost'
PORT = 8081
CHAIN_SYNC_INTERVAL = 5
RELATIVE_PATH = os.path.dirname(__file__)

TEST_PEERS = [{
    'HOST':'localhost',
    'PORT':8080
},]
