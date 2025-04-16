class SmartContract():
    def __init__(self):
        self.used_keys = {
        'a1': 0, 'a2': 0, 'a3': 0, 'a4': 0, 'a5': 0,
        'b1': 0, 'b2': 0, 'b3': 0, 'b4': 0, 'b5': 0,
        'c1': 0, 'c2': 0, 'c3': 0, 'c4': 0, 'c5': 0
    }
    
    def handle_transaction(self, transaction):
        if transaction.key in self.used_keys:

            if self.used_keys[transaction.key] != transaction.registry:
                self.used_keys[transaction.key] = transaction.registry
                return True
        else:
            raise ValueError("Invalid transaction")