# forwarder factory: create forwarder
from network.entity.consumer import Consumer
from network.entity.extension.cs_extension import CSExtension
from network.entity.extension.nfn_extension import NFNExtension
from network.entity.forwarder import Forwarder, NodeInfo
from network.entity.provider import Provider


class NAMING:
    # node type
    PROV = 'p'
    FWD = 'f'
    CSM = 'c'

    # extension type
    cs = 'cs'
    nf = 'nf'


class NodeFactory:
    def __init__(self):
        self.nodes = {}  # all instances: name -> instance ref
        self._id_counter = 0

    def get_node_by_name(self, name):
        return self.nodes[name]

    def generate_instance_by_name(self, name):
        # if name starts with 'p', it's a provider
        if name.startswith(NAMING.PROV):
            return self.get_provider(name)
        # if name starts with 'f', it's a forwarder
        elif name.startswith(NAMING.FWD):
            return self.get_forwarder(name)
        # if name starts with 'c', it's a consumer
        elif name.startswith(NAMING.CSM):
            return self.get_consumer(name)
        else:
            raise ValueError("Unknown node name")

    def get_forwarder(self, fwd_name):
        self._id_counter += 1
        fwd = Forwarder(NodeInfo(self._id_counter, fwd_name, fwd_name))

        # if forwarder name contains 'cs', this forwarder contains a ContentStore
        if NAMING.cs in fwd_name:  # ContentStore
            cs_ext = CSExtension(fwd)
            fwd.extension_slots.add_extension(cs_ext)
        if NAMING.nf in fwd_name:  # NFN
            nf_ext = NFNExtension(fwd)
            fwd.extension_slots.add_extension(nf_ext)
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
