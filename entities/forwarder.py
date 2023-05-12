import asyncio

from entities.cs import ContentStore
from entities.fib import ForwardingInformationBase
from entities.link import Link
from entities.node import Node
from entities.pit import PendingInterestTable
from named_data import NamedData


class Forwarder(Node):
    def __init__(self,
                 peers: list,
                 fib: ForwardingInformationBase,
                 pit: PendingInterestTable,
                 cs: ContentStore,
                 ):
        super().__init__(peers)
        self.fib = fib
        self.pit = pit
        self.cs = cs
        self._input_interest_queue = asyncio.Queue()
        self._input_data_queue = asyncio.Queue()
        self.enabled = True

    def enable(self, is_enabled=True):
        self.enabled = is_enabled

    def _inbound(self, nd: NamedData):
        pass

    def _outbound(self, nd: NamedData):
        pass

    def receive(self):
        """
        Pop a ND from Request Queue
        And process this Request
        :return:
        """
        nd = await self._input_data_queue.get()
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
