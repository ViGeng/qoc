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
        debug(f"Receiving interest {interest} from {last_hop_name}")
        self.last_forwarder = last_hop_ref
        await self.provide(interest)

    async def provide(self, interest: Interest):
        debug(f"Provider {self.name} is providing data for interest {interest}")
        response_data = Data(interest.name, f"Data from {self.name}")
        await self.last_forwarder.forward_data(response_data)
