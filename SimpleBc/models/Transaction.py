from abc import ABC
class Transactionx(ABC):
    def __init__(self,**kwargs):
        for chave, valor in kwargs.items():
            setattr(self, chave, valor)

    def to_dict(self):
        return self.__dict__