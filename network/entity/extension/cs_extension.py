import asyncio
from abc import ABC

from network.entity.extension.abstract_extension import AbstractExtension
from network.entity.packet.data import Data
from network.entity.packet.interest import Interest


class CSExtension(AbstractExtension, ABC):
    def __init__(self, forwarder_ref):
        self._cs = dict()
        self.forwarder_ref = forwarder_ref
        self.loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.loop)

    def add(self, data: Data):
        self._cs[data.name] = data

    def query(self, interest: Interest):
        if interest.name in self._cs:
            return self._cs[interest.name]
        return None

    async def inbound_interest_process(self, interest):
        if interest.name in self._cs:
            data = self._cs[interest.name]
            await self.forwarder_ref.forward_data(data)
            return None
        return interest

    def outbound_interest_process(self, interest) -> Interest:
        return interest

    def inbound_data_process(self, data: Data) -> Data:
        self._cs[data.name] = data
        return data

    def outbound_data_process(self, data) -> Data:
        return data
