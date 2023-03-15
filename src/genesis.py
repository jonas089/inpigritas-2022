from core.blockchain import Block, Blockchain
import os
from chainspec import RELATIVE_PATH

def reset():
    path = RELATIVE_PATH + '/data'
    print("Deleting Chain...")
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        if os.path.exists("{path}/blockchain.dat".format(path=path)):
            os.remove("{path}/blockchain.dat".format(path=path))
    Instance = Blockchain()
    Instance.new()
    genesis_Block = Block(None, None, None, None, None, None, [])
    genesis_Block.new(None)
    Instance.add_finalized_block(genesis_Block.finalize())
    print("Genesis Block generated!")
