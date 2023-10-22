from core.block import Block
from core.factory import BlockFactory

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
                serialized_block TEXT NOT NULL
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
            cursor.execute("INSERT INTO blocks (serialized_block) VALUES (?)", (serialized_block,))
            self.conn.commit()
        finally:
            self.disconnect()

    def get_block_by_index(self, height):
        try:
            self.connect()
            cursor = self.conn.cursor()
            # The height is 1-indexed based on your comment, so we're querying with height - 1
            cursor.execute("SELECT serialized_block FROM blocks WHERE id = ?", (height,))
            row = cursor.fetchone()
            return Block.deserialize(row[0]) if row else None
        finally:
            self.disconnect()

    def get_last_block(self):
        try:
            self.connect()
            cursor = self.conn.cursor()
            cursor.execute("SELECT serialized_block FROM blocks ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            return Block.deserialize(row[0]) if row else None
        finally:
            self.disconnect()