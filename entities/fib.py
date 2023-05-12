from entities.packet import Interest
from logging import debug


class FIB:
    def __init__(self):
        self._interest_table = {}  # {interest_name: forwarder_name}
        self._default_peer = None

    def get_default_peer(self):  # TODO
        if self._default_peer is None:
            raise ValueError("Default peer is not set")
        return self._default_peer

    def query(self, interest: Interest) -> str:
        """
        Query the FIB with a ND
        :param interest:
        :return: the next hop
        """
        if interest.name not in self._interest_table:
            return self.get_default_peer()
        return self._interest_table[interest.name]

    def add(self, interest_name: str, forwarder_name: str):
        """
        Add a ND to FIB
        :param interest_name:
        :param forwarder_name:
        :return:
        """
        debug(f"add {interest_name}:{forwarder_name} to FIB")
        self._interest_table[interest_name] = forwarder_name
