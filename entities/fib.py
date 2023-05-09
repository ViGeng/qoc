from entities.link import Link


class ForwardingInformationBase:
    def __init__(self):
        self.fib = {}

    def add(self, prefix: str, next_hop: Link):
        self.fib[prefix] = next_hop

    def get(self, prefix: str):
        return self.fib[prefix]

    def remove(self, prefix: str):
        del self.fib[prefix]

    def __str__(self):
        return str(self.fib)
