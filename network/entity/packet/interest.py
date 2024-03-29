from network.entity.packet.packet import Packet, MOD


class Interest(Packet):
    def __init__(self, name: str, data_name=None, func=MOD.FUNC0):
        super().__init__(name)
        self.func = func
        self.data_name = data_name

    def set_func(self, func):
        """
        :param func: input: Data, output: Data
        :return:
        """
        self.func = func

    def __str__(self):
        return f"Interest: {self.name} func: {self.func}"
