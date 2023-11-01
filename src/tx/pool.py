import sqlite3

class TxPool:
    def __init__(self, path_to_db, transactions):
        self.path_to_db = path_to_db
        self.conn = sqlite3.connect(self.path_to_db)
        self.setup_database()

        self.transactions = transactions
    # create a new transaction pool for a given block height
    def setup_database(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                sender TEXT NOT NULL,
                recipient TEXT NOT NULL,
                amount INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                signature TEXT NOT NULL,
            )
        ''')
        self.conn.commit()
    def add_transaction(self, transaction):
        pass
    # get a specific transaction from this pool
    def get_transaction_by_height(self, id):
        pass
    # get the last transaction from this pool
    def get_last_transaction(self):
        pass