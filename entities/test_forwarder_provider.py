import asyncio

from entities.consumer import Consumer
from entities.forwarder import NodeInfo, Forwarder
from entities.packet import Interest, Data
from entities.provider import Provider


def get_tasks(interest):
    forwarder_info1 = NodeInfo(1, 'forwarder1', 'forwarder1')
    forwarder = Forwarder(forwarder_info1)

    consumer = Consumer("consumer1")
    consumer.init_consumer(interest, forwarder=forwarder)

    provider = Provider("provider1")
    forwarder.add_route(interest.name, provider.name, provider)

    return consumer.get_tasks(), forwarder.get_tasks()


async def main_test_consumer2forwarder():
    """
                Interest               Interest
    ┌──────────┬───────────►┌───────────┬──────►┌──────────┐
    │ Consumer1│            │ Forwarder1│       │ Provider1│
    └──────────┘◄───────────┴───────────┘◄──────┴──────────┘
                    Data                 Data
    :return:
    """
    interest = Interest(
        name='/provider1/hello',
    )
    consumer_tasks, forwarder_tasks = get_tasks(interest)
    await asyncio.gather(*consumer_tasks, *forwarder_tasks)


if __name__ == '__main__':
    asyncio.run(main_test_consumer2forwarder())

