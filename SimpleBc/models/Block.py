from abc import ABC
import hashlib
import json
from cryptography.hazmat.primitives import hashes

class Blockx(ABC):
    def __init__(self,**kwargs):
        for chave, valor in kwargs.items():
            setattr(self, chave, valor)

    def hash_block(self):
        block_str = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()
    
    def get_hash(self):
        return self.hash_block()