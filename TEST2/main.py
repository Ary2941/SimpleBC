import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime

from models.Transaction import Transaction
from models.SmartContract import SmartContract
from models.Wallet import Wallet


from SimpleBc.objects.Blockchain import Blockchain

blockchain = Blockchain(transaction_model=Transaction,smart_contract_model=SmartContract,wallet_model=Wallet)

john = Wallet()

transaction = {
    "user": john.public_key_hex(),
    "registry": 1,
    "key": "a1",
    "timestamp": datetime.now().isoformat()
}
transaction["signature"] = john.sign(transaction)
blockchain.add_transaction(transaction)


transaction = {
    "user": john.public_key_hex(),
    "registry": 0,
    "key": "a1",
    "timestamp": datetime.now().isoformat()
}
transaction["signature"] = john.sign(transaction)
blockchain.add_transaction(transaction)


blockchain.create_block()

transaction = {
    "user": john.public_key_hex(),
    "registry": 1,
    "key": "a1",
    "timestamp": datetime.now().isoformat()
}
transaction["signature"] = john.sign(transaction)
blockchain.add_transaction(transaction)


print(blockchain.chain)