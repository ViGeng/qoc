from network.entity.packet.packet import Packet


class Data(Packet):
    def __init__(self, name: str, data_content: str = None):
        super().__init__(name)
        self.data_content = data_content

    def __str__(self):
        return f"Data({self.name}, {self.data_content})"
