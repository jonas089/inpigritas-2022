import os
BLOCKTIME = os.getenv("INPIG_BLOCKTIME", default=30) # 30 seconds
ACCOUNT = os.getenv("INPIG_ACCOUNT", default='0x00') # premine address
PREMINE = os.getenv("INPIG_PREMINE", default='') # premine amount)
HOST = os.getenv("INPIG_HOST", default='0.0.0.0')
PORT = os.getenv("INPIG_PORT", default=8080)
CHAIN_SYNC_INTERVAL = os.getenv("INPIG_CHAIN_SYNC_INTERVAL", default=5)
RELATIVE_PATH = os.path.dirname(__file__)
TEST_PEERS = [{
    'HOST': HOST,
    'PORT': PORT
}]
