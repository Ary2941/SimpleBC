# OBS: Atributos devem ser serializáveis em JSON
import copy

class Transaction:
    def __init__(self,user,registry,key,timestamp,signature):
        self.user = user
        self.registry = registry
        self.key = key
        self.timestamp = timestamp
        self.signature = signature

    def to_dict(self):
        dict_respresentation = copy.deepcopy(self.__dict__)
        dict_respresentation["signature"] = ""
        return dict_respresentation

'''
registry:
    0 - Tirei chave
    1 - Coloquei chave
'''