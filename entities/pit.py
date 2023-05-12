from entities.packet import Interest, Data
from logging import debug


class PIT:
    def __init__(self):
        self.table: dict = {}

    def add(self, interest: Interest, forwarder_name: str):
        debug(f"add {interest.name}:{forwarder_name} to PIT")
        self.table[interest.name] = forwarder_name

    def query_by_interest(self, interest: Interest) -> str:
        return self.table[interest.name]

    def query_by_data(self, data: Data) -> str:
        return self.table[data.name]

    def pop_by_data(self, data: Data) -> str:
        last_hop_name = self.table[data.name]
        del self.table[data.name]
        debug(f"pop {data.name}:{last_hop_name} from PIT")
        return last_hop_name

    def remove(self, interest: Interest):
        del self.table[interest]

    def __str__(self):
        return str(self.table)
