from block import Block
from factory import BlockFactory

class BlockChain:
    def __init__(self, path_to_db):
        self.path = path_to_db
        self.factory = BlockFactory()
        
    def save_block(self, block):
        # save a new block
        pass

    def get_block_by_index(self, height):
        # return a block at a given height, starting at i=1
        pass

    def get_last_block(self):
        # return the last added block 
        pass