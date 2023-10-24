from core.block import Block
from core.blockchain import BlockChain

block = Block(
    0,
    [],
    "timestamp",
    "next_timestamp",
    "hash",
    "next_hash",
    "prev_hash"
)

blockchain = BlockChain('./inpigritas.db')
blockchain.save_block(block.serialize())

_block = blockchain.get_last_block()
print("Last block in chain: ", _block)