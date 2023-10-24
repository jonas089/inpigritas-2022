from core.block import Block
from core.factory import BlockFactory
import sqlite3

class BlockChain:
    def __init__(self, path_to_db):
        self.factory = BlockFactory()
        self.path_to_db = path_to_db
        self.conn = sqlite3.connect(self.path_to_db)
        self.setup_database()
    
    def setup_database(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blocks (
                id INTEGER PRIMARY KEY,
                height INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                next_timestamp TEXT NOT NULL,
                hash TEXT NOT NULL,
                next_hash TEXT NOT NULL,
                prev_hash TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    
    def connect(self):
        if not self.conn:
            self.conn = sqlite3.connect(self.path_to_db)
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def save_block(self, serialized_block):
        try:
            # save a new block
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO blocks (height, timestamp, next_timestamp, hash, next_hash, prev_hash) VALUES (?,?,?,?,?,?)", 
            (
                serialized_block['height'],
                serialized_block['timestamp'],
                serialized_block['next_timestamp'],
                serialized_block['hash'],
                serialized_block['next_hash'],
                serialized_block['prev_hash']
            ))
            self.conn.commit()
        finally:
            self.disconnect()

    def get_block_by_height(self, height):
        try:
            self.connect()
            cursor = self.conn.cursor()
            # The height is 1-indexed based on your comment, so we're querying with height - 1
            cursor.execute("SELECT * FROM blocks WHERE height = ?", (height))
            row = cursor.fetchone()
            block = Block(
                row[1],
                [],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6]
            )
            return Block if row else None
        finally:
            self.disconnect()

    def get_last_block(self):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM blocks ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            block = Block(
                row[1],
                [],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6]
            )
            return Block if row else None
        finally:
            self.disconnect()