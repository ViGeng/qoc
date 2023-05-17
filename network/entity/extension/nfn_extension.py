from abc import ABC

from logging import debug
from network.entity.extension.abstract_extension import AbstractExtension
from network.entity.packet.data import Data
from network.entity.packet.interest import Interest
from network.entity.packet.packet import MOD


class NFNExtension(AbstractExtension, ABC):
    def __init__(self, forwarder_ref):
        super().__init__()
        self.forwarder_ref = forwarder_ref

    async def inbound_interest_process(self, interest) -> Interest:
        # if this is a computation request
        if interest.func is not MOD.FUNC0 and interest.data_name:
            debug(f"NFNExtension: inbound_interest_process: computing {interest}")
            # TODO: now we assume this a function rather than a name of program data
            func = interest.func
            # TODO: now we assume this a function rather than a name of program data
            para = interest.data_name
            data_content = func(para)
            data = Data(interest.name, data_content)
            await self.forwarder_ref.forward_data(data)
            return None
        return interest

    def inbound_data_process(self, data) -> Data:
        return data

    def outbound_interest_process(self, interest) -> Interest:
        return interest

    def outbound_data_process(self, data) -> Data:
        return data

    def __str__(self):
        return f"NFNExtension"
