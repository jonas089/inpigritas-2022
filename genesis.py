from core.blockchain import Block, Blockchain
import os

if not os.path.exists('./data'):
    os.mkdir('./data')

Instance = Blockchain()
Instance.new()
genesis_Block = Block(None, None, None, None, None, None, [])
genesis_Block.new(None)
Instance.add_finalized_block(genesis_Block.finalize())
