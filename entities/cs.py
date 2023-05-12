class ContentStore:
    """
            CS (Content Store): caches received data packets, and when an interest arrives,
        the router first checks the CS to see if there is a matching data packet.
        If so, the data packet is returned; otherwise, the interest is added to the PIT.
    """
    def __init__(self):
        self._content = {}

    def add(self, content):
        self._content[content.id] = content

    def get(self, id):
        return self._content[id]