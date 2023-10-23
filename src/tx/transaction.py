class Tx:
    def __init__(self, sender, recipient, amount, timestamp, signature):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp
        self.signature = signature
    
    def serialize(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature
        }

    def deserialize(tx_serialized):
        return Tx(
            tx_serialized["sender"], 
            tx_serialized["recipient"], 
            tx_serialized["amount"], 
            tx_serialized["timestamp"],
            tx_serialized["signature"]
        )

    def verify(self):
        pass