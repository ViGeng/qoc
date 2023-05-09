class ContentStore:
    def __init__(self):
        self._content = {}

    def add(self, content):
        self._content[content.id] = content

    def get(self, id):
        return self._content[id]