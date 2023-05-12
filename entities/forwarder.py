import asyncio
import logging
from logging import debug

from entities.cs import CS
from entities.faces import Faces
from entities.fib import FIB
from entities.packet import Data, Interest
from entities.pit import PIT

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
        self.node_info = node_info
        self._incoming_interest_queue = asyncio.Queue()
        self._incoming_data_queue = asyncio.Queue()
        self.fib = FIB()
        self.pit = PIT()
        self.cs = CS()
        self.faces = Faces()
        self.forwarding_interest_enabled = True
        self.forwarding_data_enabled = True
        self.send_hello_interest_enabled = True

    def add_peer(self, peer):
        self.faces.add(peer.node_info.name, peer)

    async def forward_interest(self, interest: Interest, last_hop_name: str, last_hop_ref):
        """
        Receive an Interest from outside.
        This is usually called by other forwarders.
        :param last_hop_name:
        :param last_hop_ref: the reference of the last hop forwarder TODO: remove this, use simulator links instead
        :param interest: the interest will be sent to the next hop
        :return: None
        """
        debug(f"forwarding interest {interest} from {last_hop_name}")
        self.fib.add(interest.name, last_hop_name)
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
            self.pit.add(interest, last_hop_name)
            response = self.cs.query(interest)
            if response is None:
                debug(f"No local data for {interest}, forwarding")
                return interest
            else:
                debug(f"Found local data for {interest}, sending back")
                self.send_data(response)

    def send_interest(self, interest: Interest):
        peer_name = self.fib.query(interest)
        peer = self.faces.query_by_peer_name(peer_name)
        debug(f"send interest {interest} to {peer_name}")
        peer.forward_interest(interest, self.node_info.name, self)

    async def forwarding_interest(self):
        debug("Coroutine forwarding_interest started")
        while self.forwarding_interest_enabled:
            interest = await self.receive_interest()
            self.send_interest(interest)

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
        debug(f"received data {data}")
        return data

    async def forwarding_data(self):
        debug("Coroutine forwarding_data started")
        while self.forwarding_data_enabled:
            data: Data = await self.receive_data()
            peer_name = self.pit.pop_by_data(data)
            peer = self.faces.query_by_peer_name(peer_name)
            peer.forward_data(data)

    def send_data(self, data: Data):
        """
        Receive a NamedData from outside.
        This is usually called by other forwarders.
        :return: None
        """
        incoming_peer_name = self.pit.pop_by_data(data)
        incoming_peer = self.faces.query_by_peer_name(incoming_peer_name)
        debug(f"send data {data} to {incoming_peer_name}")
        incoming_peer.forward_data(data)

    async def dog(self):
        while True:
            await asyncio.sleep(10)
            debug(f"Watching DOG: {self.node_info.name} is alive, woo woo !")

    def get_tasks(self) -> list:
        return [
            asyncio.create_task(self.forwarding_interest()),
            asyncio.create_task(self.forwarding_data()),
            asyncio.create_task(self.dog()),
        ]


async def initialize():
    # TODO: implement a initializer
    # build network topology
    node_info1 = NodeInfo(1, 'node1', 'node1')
    forwarder1 = Forwarder(node_info1)

    node_info2 = NodeInfo(2, 'node2', 'node2')
    forwarder2 = Forwarder(node_info2)

    forwarder1.add_peer(forwarder2)
    forwarder2.add_peer(forwarder1)

    # build interest and data
    interest_hello = Interest(
        name='/node2/hello',
    )
    data_hi = Data(
        name="/node2/hello",
        data_content='hello world!',
    )

    # init nodes
    forwarder1.fib.add(interest_hello.name, forwarder2.node_info.name)
    forwarder1.faces.add(forwarder2.node_info.name, forwarder2)
    forwarder2.cs.add(interest_hello, data_hi)
    await asyncio.gather(*forwarder1.get_tasks(), *forwarder2.get_tasks())

if __name__ == '__main__':
    asyncio.run(initialize())