from entities.entity import Entity
from entities.forwarder import Forwarder
from entities.node import Node


class LinkCondition:
    def __init__(self, delay, throughput):
        self._delay = delay
        self._throughput = throughput
        # variation rate and so on


class Link(Entity):
    '''
    Link represents the edges in a networking graph
    A link can only connect two nodes.
    The link is undirected(full duplex) but weighted(delay, throughput, and other conditions).
    '''

    def __init__(self, node1: Node, node2: Node, weight: LinkCondition, value: int = 1):
        super().__init__()
        self.value = value
        self._nodes = (node1, node2)
        self._weight = weight

    def get_peer_node(self, self_node: Node):
        if self._nodes[0] == self_node:
            return self._nodes[1]
        return self._nodes[0]

    def transmit(self, nd, self_node: Node):
        peer = self.get_peer_node(self_node)
        # if peer is an instance of Fowarder, then forward the packet
        if isinstance(peer, Forwarder):
            peer.forward(nd)
        else:
            raise Exception("The peer node is not a forwarder")