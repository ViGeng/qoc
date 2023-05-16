# forwarder factory: create forwarder
from network.entity.consumer import Consumer
from network.entity.forwarder import Forwarder, NodeInfo
from network.entity.provider import Provider


class NodeFactory:
    def __init__(self):
        self.nodes = {}  # all instances: name -> instance ref
        self._id_counter = 0

    def get_node_by_name(self, name):
        return self.nodes[name]

    def generate_instance_by_name(self, name):
        # if name starts with 'p', it's a provider
        if name.startswith('p'):
            return self.get_provider(name)
        # if name starts with 'f', it's a forwarder
        elif name.startswith('f'):
            return self.get_forwarder(name)
        # if name starts with 'c', it's a consumer
        elif name.startswith('c'):
            return self.get_consumer(name)
        else:
            raise ValueError("Unknown node name")

    def get_forwarder(self, fwd_name):
        self._id_counter += 1
        fwd = Forwarder(NodeInfo(self._id_counter, fwd_name, fwd_name))
        self.nodes[fwd_name] = fwd
        return fwd

    def get_consumer(self, consumer_name) -> Consumer:
        self._id_counter += 1
        consumer = Consumer(consumer_name)
        self.nodes[consumer_name] = consumer
        return consumer

    def get_provider(self, provider_name) -> Provider:
        self._id_counter += 1
        provider = Provider(provider_name)
        self.nodes[provider_name] = provider
        return provider
