import os
BLOCKTIME = os.getenv("INPIG_BLOCKTIME", default=30) # 30 seconds
ACCOUNT = os.getenv("INPIG_ACCOUNT", default='0x00') # premine address
PREMINE = os.getenv("INPIG_PREMINE", default='') # premine amount)
CONFIRMATIONS = 3 # 3 block confirmations for every transaction
HOST = os.getenv("INPIG_HOST", default='0.0.0.0')
PORT = os.getenv("INPIG_PORT", default=8080)

INPIG_PEER_HOST = os.getenv("INPIG_PEER_HOST", default='localhost')
INPIG_PEER_PORT = os.getenv("INPIG_PEER_PORT", default=8080)
CHAIN_SYNC_INTERVAL = os.getenv("INPIG_CHAIN_SYNC_INTERVAL", default=5)
RELATIVE_PATH = os.path.dirname(__file__)
TEST_PEERS = [{
    'HOST': INPIG_PEER_HOST,
    'PORT': INPIG_PEER_PORT
}]
