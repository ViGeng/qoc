from network.entity.packet.data import Data
from network.entity.packet.interest import Interest


class CS:
    def __init__(self):
        self._cs = dict()

    def add(self, data: Data):
        self._cs[data.name] = data

    def query(self, interest: Interest):
        if interest.name in self._cs:
            return self._cs[interest.name]
        return None
