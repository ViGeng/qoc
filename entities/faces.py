from entities.link import Link


class Faces:
    """
    Face: represents a network interface,
        which can be a physical or virtual interface for sending
        and receiving interest and data packets.
    """
    def __init__(self, links: [Link]):
        self._links = links

