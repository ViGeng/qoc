from logging import debug

from entities.forwarder import Forwarder
from entities.packet import Data, Interest


class Provider:
    def __init__(self, name):
        self.last_forwarder = None
        self.name = name
        self.is_inited = False

    async def forward_interest(self,
                               interest: Interest,
                               last_hop_name: str,
                               last_hop_ref: Forwarder
                               ):
        debug(f"{self}: Receiving interest {interest} from {last_hop_name}")
        self.last_forwarder = last_hop_ref
        await self.provide(interest)

    async def provide(self, interest: Interest):
        debug(f"{self}: is providing data for interest {interest}")
        response_data = Data(interest.name, f"Data from {self.name}")
        debug(f"{self}: is forwarding data {response_data} to {self.last_forwarder}")
        await self.last_forwarder.forward_data(response_data)

    def __str__(self):
        return f"Provider-{self.name}"
