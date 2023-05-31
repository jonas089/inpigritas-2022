from blockchain import Blockchain
'''
    TBD: use Blockchain class to calculate current Balance.
    Also include Transactions from the Txpool to prevent double-spending.
'''

'''
    Balance is just the result of all incoming <- and all outgoing -> transactions
    in all accepted blocks. There may be a pending balance at times. It doesn't make
    sense to implement this before finishing the database & synchronisation logic
'''
class Ledger:
    def __init__(self, account):
        self.account = account
