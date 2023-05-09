import asyncio

from entities.link import Link
from entities.node import Node
from named_data import NamedData


class Forwarder(Node):
    def __init__(self, links: list[Link]):
        super().__init__(links)
        # FIB (Forwarding Information Base):
        # stores prefix-to-next-hop mappings
        # and supports prefix matching and longest-prefix matching.
        self.fib = None
        # PIT (Pending Interest Table): stores pending interests,
        # and when a data packet arrives,
        # the router looks up the PIT to find the corresponding interest
        # and forwards the data to the source of that interest.
        self.pit = None
        # CS (Content Store): caches received data packets, and when an interest arrives,
        # the router first checks the CS to see if there is a matching data packet.
        # If so, the data packet is returned; otherwise, the interest is added to the PIT.
        self.cs = None
        # Face: represents a network interface,
        # which can be a physical or virtual interface for sending
        # and receiving interest and data packets.
        self.faces = None
        # 	Strategy: specifies the forwarding strategy for interests,
        # 	such as random forwarding or shortest-path forwarding.
        self.strategy = None
        self.executor = None
        self._input_request_queue = asyncio.Queue()
        self.enabled = True

    def enable(self, is_enabled = True):
        self.enabled = is_enabled

    def _inbound(self, nd:NamedData):
        pass

    def _outbound(self, nd:NamedData):
        pass

    def receive(self):
        """
        Pop a ND from Request Queue
        And process this Request
        :return:
        """
        nd = await self._input_request_queue.get()
        self._outbound(nd)
        return nd

    def forward(self, nd: NamedData):
        """
        Receive a NamedData from outside.
        This is usually called by other forwarders.
        :param nd: received ND
        :return: None
        """
        self._inbound(nd)
        await self._input_request_queue.put(nd)

    def send(self, nd: NamedData):
        link = self.fib.query(nd)
        link.transmit(nd)

    async def forwarding(self):
        while self.Enabled:
            nd = await self.receive()  # await other forwarder to foward requests to this node
            self.send(nd)

