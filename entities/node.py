from entities.entity import Entity
from entities.forwarder import Forwarder
from entities.link import Link


class Node(Entity):
    '''
    A network consists of nodes and edges. Nodes are connected by edges.
    This is a Node class which represents a computer/forwarder/router in a network.
    '''
    def __init__(self, peers: list):
        self.peers = peers  # supposed to be nodes

