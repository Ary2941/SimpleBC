import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime

from SimpleBc.objects.Blockchain import Blockchain

blockchain = Blockchain()

blockchain.add_transaction({
    "user": "Alice",
    "registry": 1,
    "key": "a1",
    "timestamp": datetime.now().isoformat()
})

blockchain.add_transaction({
    "user": "Bruno",
    "registry": 0,
})

blockchain.create_block()

blockchain.add_transaction({
    "Rocambole": True,
})

blockchain.create_block()

print(blockchain.chain)