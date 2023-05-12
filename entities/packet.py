class Packet:
    def __init__(self, name: str):
        self.name = name

    pass


class Interest(Packet):
    def __init__(self, name: str):
        super().__init__(name)


class Data(Packet):
    def __init__(self, name: str, data_content: str = None):
        super().__init__(name)
        self.data_content = data_content

    def __str__(self):
        return f"Data({self.name}, {self.data_content})"
