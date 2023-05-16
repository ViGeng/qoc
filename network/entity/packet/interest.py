from network.entity.packet.packet import Packet


class Interest(Packet):
    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self):
        return f"Interest({self.name})"