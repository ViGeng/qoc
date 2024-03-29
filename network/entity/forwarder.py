import asyncio
import logging
from logging import debug

from network.entity.component.extension_slots import ExtensionSlots
from network.entity.component.faces import Faces
from network.entity.component.fib import FIB
from network.entity.component.pit import PIT
from network.entity.packet.data import Data
from network.entity.packet.interest import Interest

# config logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s'
)


class NodeInfo:
    """
    NodeInfo is a struct that contains information about a node.
    """

    def __init__(self,
                 node_id: int,
                 name: str,
                 description: str,
                 ):
        self.node_id = node_id
        self.name = name
        self.description = description


class Forwarder:
    """
    Forwarder is a node that forwards messages to other nodes.
    """

    def __init__(self, node_info: NodeInfo):
        self.route = None
        self.node_info = node_info
        self._incoming_interest_queue = asyncio.Queue()
        self._incoming_data_queue = asyncio.Queue()
        self.fib = FIB()
        self.pit = PIT()
        self.faces = Faces()
        self.extension_slots = ExtensionSlots()
        self.forwarding_interest_enabled = True
        self.forwarding_data_enabled = True
        self.send_hello_interest_enabled = True

    def add_peer(self, peer):
        self.faces.add(peer.node_info.name, peer)

    def add_route(self, prefix, peer_name, peer_ref):
        self.fib.add(prefix, peer_name)
        self.faces.add(peer_name, peer_ref)

    def set_route(self, route):
        self.route = route

    async def forward_interest(self, interest: Interest, last_hop_name: str, last_hop_ref):
        """
        Receive an Interest from outside.
        This is usually called by other forwarders.
        :param last_hop_name:
        :param last_hop_ref: the reference of the last hop forwarder TODO: remove this, use simulator links instead
        :param interest: the interest will be sent to the next hop
        :return: None
        """
        debug(f"Forwarder-{self.node_info.name}: forwarding interest {interest} from {last_hop_name}")
        self.pit.add(interest, last_hop_name)
        self.faces.add(last_hop_name, last_hop_ref)
        await self._incoming_interest_queue.put((interest, last_hop_name))

    async def receive_interest(self) -> Interest:
        """
        Pop an Interest from Queue
        And process it
        :return: interest that is not in the CS
        """
        while True:
            interest, last_hop_name = await self._incoming_interest_queue.get()
            debug(f"Forwarder-{self.node_info.name}: Received interest {interest} from {last_hop_name}")
            interest = await self.extension_slots.inbound_interest_process(interest)
            if interest is None:
                debug(f"Forwarder-{self.node_info.name}: interest handled by extension, wait for next interest")
                continue
            return interest

    async def send_interest(self, interest: Interest):
        # peer_name = self.fib.query(interest)
        # peer = self.faces.query_by_peer_name(peer_name)
        peer = self.route.query_route(interest.name, self.node_info.name)
        debug(f"Forwarder-{self.node_info.name}: send interest {interest} to {peer}")
        self.extension_slots.outbound_interest_process(interest)
        await peer.forward_interest(interest, self.node_info.name, self)

    async def forwarding_interest(self):
        debug(f"Forwarder-{self.node_info.name}: Coroutine forwarding_interest started")
        while self.forwarding_interest_enabled:
            interest = await self.receive_interest()
            await self.send_interest(interest)

    async def forward_data(self, data: Data):
        """
        Receive a Data from outside.
        This is usually called by other forwarders.
        :param data: the data will be sent to the next hop
        :return: None
        """
        await self._incoming_data_queue.put(data)

    async def receive_data(self) -> Data:
        """
        Pop a ND from Queue
        And process this Request
        :return:
        """
        data = await self._incoming_data_queue.get()
        data = self.extension_slots.inbound_data_process(data)
        debug(f"Forwarder:{self.node_info.name}: received data {data}")
        return data

    async def forwarding_data(self):
        debug(f"Forwarder-{self.node_info.name}: Coroutine forwarding_data started")
        while self.forwarding_data_enabled:
            data: Data = await self.receive_data()
            peer_name = self.pit.pop_by_data(data)
            peer = self.faces.query_by_peer_name(peer_name)
            await peer.forward_data(data)

    async def send_data(self, data: Data):
        """
        Receive a NamedData from outside.
        This is usually called by other forwarders.
        :return: None
        """
        incoming_peer_name = self.pit.pop_by_data(data)
        incoming_peer = self.faces.query_by_peer_name(incoming_peer_name)
        data = self.extension_slots.outbound_data_process(data)
        debug(f"Forwarder-{self.node_info.name}: send data {data} to {incoming_peer_name}")
        await incoming_peer.forward_data(data)

    async def dog(self):
        while True:
            await asyncio.sleep(10)
            debug(f"Forwarder-{self.node_info.name}: Watching DOG is alive, woo woo !")

    def get_tasks(self) -> list:
        return [
            asyncio.create_task(self.forwarding_interest()),
            asyncio.create_task(self.forwarding_data()),
            asyncio.create_task(self.dog()),
        ]

    def __str__(self):
        return f"Forwarder-{self.node_info.name}"

