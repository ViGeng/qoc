class PendingInterestTable():
    def __init__(self):
        self.table = {}

    def add(self, interest):
        self.table[interest.name] = interest

    def remove(self, interest):
        del self.table[interest.name]

    def get(self, name):
        return self.table[name]

    def __str__(self):
        return str(self.table)