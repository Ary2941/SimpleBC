# no_core_da_sua_biblioteca.py
import json
from SimpleBc.models.Block import Blockx
from SimpleBc.models.Transaction import Transactionx
from SimpleBc.models.SmartContract import SmartContractx
from SimpleBc.models.Wallet import Walletx

class Blockchain:
    def __init__(self, 
            transaction_model = Transactionx,
            smart_contract_model = SmartContractx,
            wallet_model = Walletx,
            block_model = Blockx
            ):
        self.transaction_model = transaction_model
        self.smart_contract_model = smart_contract_model()
        self.wallet_model = wallet_model()
        self.block_model = block_model
        self.chain = []
        self.current_transactions = []

    def add_transaction(self, tx_data):
        tx = self.transaction_model(**tx_data)
        if not self.wallet_model.signature_valid(tx):
            raise ValueError("invalid signature")
        self.smart_contract_model.handle_transaction(tx)
        self.current_transactions.append(tx)
        
    def create_block(self,block = None,previous_hash="0"):

        if block is None:
            if not self.chain == []:
                previous_hash = self.chain[-1].hash

            block = self.block_model(
                prev = previous_hash,
                index =  len(self.chain) + 1,
                transactions = [tx.to_dict() for tx in self.current_transactions],
            )

            block.hash = block.hash_block()

            if block.hash == previous_hash:
                raise ValueError("Block hash is equal to previous hash.")
        
        if len(block.transactions) == 0: 
            raise ValueError("Block has no transactions.")
        print(f"BLOCO {block.hash} criado")
        self.chain.append(block)
        self.current_transactions = []
        return block
