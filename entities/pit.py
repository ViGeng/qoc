class PendingInterestTable:
    """
    PIT (Pending Interest Table): stores pending interests,
        and when a data packet arrives,
        the router looks up the PIT to find the corresponding interest
        and forwards the data to the source of that interest.
    """
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