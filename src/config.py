import os
BLOCKTIME = os.getenv("INPIG_BLOCKTIME", default=30) # 30 seconds
CONFIRMATIONS = 3 # 3 block confirmations for every transaction
NODE_SYNC_INTERVAL = os.getenv("INPIG_NODE_SYNC_INTERVAL", default=5)

ACCOUNT = os.getenv("INPIG_ACCOUNT", default='0x00') # premine address
PREMINE = os.getenv("INPIG_PREMINE", default='') # premine amount)

HOST = os.getenv("INPIG_HOST", default='0.0.0.0')
PORT = os.getenv("INPIG_PORT", default=8080)

INPIG_PEER_HOST = os.getenv("INPIG_PEER_HOST", default='localhost')
INPIG_PEER_PORT = os.getenv("INPIG_PEER_PORT", default=8080)

RELATIVE_PATH = os.path.dirname(__file__)
PATH_TO_DB = os.getenv("INPIG_DB_PATH", default="/Users/chef/Desktop/inpigritas-2022/src/inpigritas.db")

TEST_PEERS = [{
    'HOST': INPIG_PEER_HOST,
    'PORT': INPIG_PEER_PORT
}]