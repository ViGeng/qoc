class Packet:
    def __init__(self, name: str):
        self.name = name


class MOD:
    """
    (d0, f0) -> d0
    (d0, f1) -> d1
    (d1, f2) -> d2 -> (d2, f0)
    (f1, f0) -> f1
    """
    FUNC0 = lambda x: x  # this is original function, can not be decoupled anymore
