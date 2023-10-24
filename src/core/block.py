import sqlite3

class Block:
    def __init__(self, height, transactions, timestamp, next_timestamp, hash, next_hash, prev_hash):
        self.height = height
        self.transactions = transactions
        self.timestamp = timestamp
        self.next_timestamp = next_timestamp
        self.hash = hash
        self.next_hash = next_hash
        self.prev_hash = prev_hash
    
    def serialize(self):
        return {
            "height": self.height,
            # transactions need to be serialized seperately
            "transactions": self.transactions,
            "timestamp": self.timestamp,
            "next_timestamp": self.next_timestamp,
            "hash": self.hash,
            "next_hash": self.next_hash,
            "prev_hash": self.prev_hash
        }
    
    def deserialize(block_serialized):
        return Block(
            block_serialized["height"],
            block_serialized["transactions"],
            block_serialized["timestamp"],
            block_serialized["next_timestamp"],
            block_serialized["hash"],
            block_serialized["next_hash"],
            block_serialized["prev_hash"]
        )

    def verify(self):
        pass
