import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime

from models.Transaction import Transaction


from SimpleBc.objects.Blockchain import Blockchain

blockchain = Blockchain(transaction_model=Transaction)

blockchain.add_transaction({
    "user": "Alice",
    "registry": 1,
    "key": "a1",
    "timestamp": datetime.now().isoformat()
})

blockchain.add_transaction({
    "user": "Alice",
    "registry": 0,
    "key": "a1",
    "timestamp": datetime.now().isoformat()
})

blockchain.create_block()

blockchain.add_transaction({
    "user": "Alice",
    "registry": 1,
    "key": "a1",
    "timestamp": datetime.now().isoformat()
})

blockchain.create_block()

print(blockchain.chain)