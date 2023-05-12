from entities.packet import Interest, Data


class CS:
    def __init__(self):
        self._cs = dict()

    def add(self, interest: Interest, data: Data):
        self._cs[interest] = data

    def query(self, interest: Interest):
        if interest in self._cs:
            return self._cs[interest]
        return None
