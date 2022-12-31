from core.transfer import Transfer
from core.blockchain import Block, Blockchain
from core.accounts import Keys
import time
from chainspec import BLOCKTIME
# 1. initialize a new, empty Blockchain instance
Instance = Blockchain()
Instance.new()
# 2. Key instance
_Keys = Keys()
# 3. Genesis Block
timestamp = time.time()
genesis_Block = Block(None, None, None, None, None, None, [])
genesis_Block.new(None)
Instance.add_finalized_block(genesis_Block.finalize())
# 4. Send a Transaction that is to be included in Block #1
tx = Transfer('sender', 'recipient', 10, None, None, None, None, 1, _Keys)
tx.new()
tx.add_to_pool()
# 5. Create Block #1 that should hold the transfer
prev_Block_Dict = Instance.chain[0] # = Genesis Block
prev_Block = Block(prev_Block_Dict['index'], prev_Block_Dict['timestamp'], prev_Block_Dict['next_timestamp'], prev_Block_Dict['block_hash'], prev_Block_Dict['next_hash'], prev_Block_Dict['prev_hash'], prev_Block_Dict['transfers'])
new_Block = Block(None, None, None, None, None, None, [])
new_Block.new(prev_Block)
Instance.add_finalized_block(new_Block.finalize())
print(Instance.chain)
print("Transaction valid: ", tx.validate())
