import asyncio
from logging import debug

from network.entity.packet.data import Data
from network.entity.packet.interest import Interest


class Consumer:
    def __init__(self, name):
        self.interest = None
        self.forwarder = None
        self.name = name
        self.is_inited = False
        self.is_enabled = True
        self.counter = 0
        self.sending_period = 3

    async def send_interest(self):
        if not self.is_inited:
            raise ValueError("Consumer not inited")
        debug(f"Consumer {self.name} is sending interest {self.interest} to forwarder: {self.forwarder.node_info.name}")
        await self.forwarder.forward_interest(self.interest, self.name, self)

    async def forward_data(self, data):
        """
        Receive data from forwarder
        :param data:
        :return:
        """
        if not self.is_inited:
            raise ValueError("Consumer not inited")
        debug(f"Consumer-{self.name}: received data {data}")
        await asyncio.sleep(1)
        self.consume(data)

    def consume(self, data: Data):
        debug(f"Consumer-{self.name}: consumed data {data}")

    def init_consumer(self, interest: Interest, forwarder, sending_period):
        self.interest = interest
        self.forwarder = forwarder
        self.sending_period = sending_period
        self.is_inited = True
        debug(
            f"Consumer-{self.name}: inited with interest {self.interest} and forwarder {self.forwarder.node_info.name}")

    async def sending_interest(self):
        while self.is_enabled:
            await asyncio.sleep(self.sending_period)
            await self.send_interest()
            debug(f"Consumer-{self.name}: sent interest {self.interest}")

    async def dog(self):
        while True:
            await asyncio.sleep(30)
            debug(f"Consumer-{self.name}: is alive, woo woo !")

    def get_tasks(self):
        return [
            asyncio.create_task(self.sending_interest()),
            asyncio.create_task(self.dog()),
        ]
