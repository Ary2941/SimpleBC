# OBS: Atributos devem ser serializáveis em JSON
class Transaction:
    def __init__(self,user,registry,key,timestamp):
        self.user = user
        self.registry = registry
        self.key = key
        self.timestamp = timestamp

    def to_dict(self):
        return self.__dict__

'''
registry:
    0 - Tirei chave
    1 - Coloquei chave
'''