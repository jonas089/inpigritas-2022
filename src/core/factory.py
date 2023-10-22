from Crypto.Hash import SHA384

class BlockFactory:
    def create_new_block(self, index, prev_hash, transactions, timestamp, next_timestamp):
        # compute next timestamp 
        next_timestamp = timestamp + BLOCK_TIME
        # compute hash
        hash = self.compute_hash(index, timestamp, next_timestamp, prev_hash)
        next_hash = self.compute_next_hash(index, next_timestamp, hash)
        return Block(
            transactions,
            timestamp,
            next_timestamp,
            hash,
            next_hash
        )

    def compute_hash(self, index, timestamp, next_timestamp, prev_hash):
        hash = hashlib.sha384()
        hash.update('{index}{prev_hash}{timestamp}{next_timestamp}'.format(
            index=index, 
            prev_hash=prev_hash, 
            timestamp=timestamp, 
            next_timestamp=next_timestamp
        ).encode('utf-8'))
        return hash

    def compute_next_hash(self, index, timestamp, hash):
        next_timestamp = timestamp + BLOCK_TIME
        hash = hashlib.sha384()
        hash.update('{index}{prev_hash}{timestamp}{next_timestamp}'.format(
            index=index,
            prev_hash=prev_hash,
            timestamp=timestamp,
            next_timestamp=next_timestamp
        ).encode('utf-8'))
        return hash