from logging import debug, error


class Faces:
    def __init__(self):
        self._faces = {}  # {peer_name: peer_ref}

    def add(self, peer_name: str, peer_ref):
        self._faces[peer_name] = peer_ref  # LRU can be used here to main a fixed size of table

    def query_by_peer_name(self, peer_name: str):
        if peer_name not in self._faces:
            error(f"Face {peer_name} not exists")
            raise Exception("Face {} not exists".format(peer_name))
        return self._faces[peer_name]
