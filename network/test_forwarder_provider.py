import asyncio

from network.entity.consumer import Consumer
from network.entity.forwarder import NodeInfo, Forwarder
from network.entity.packet import Interest
from network.entity.provider import Provider


def get_tasks(interest):
    forwarder_info1 = NodeInfo(1, 'forwarder1', 'forwarder1')
    forwarder = Forwarder(forwarder_info1)

    consumer = Consumer("consumer1")
    consumer.init_consumer(interest, forwarder=forwarder)

    provider = Provider("provider1")
    forwarder.add_route(interest.name, provider.name, provider)

    return consumer.get_tasks(), forwarder.get_tasks()


async def main_test_cfp():
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


def get_tasks2(interest) -> list:
    forwarder_info1 = NodeInfo(1, 'forwarder1', 'forwarder1')
    forwarder1 = Forwarder(forwarder_info1)

    forwarder_info2 = NodeInfo(2, 'forwarder2', 'forwarder2')
    forwarder2 = Forwarder(forwarder_info2)

    consumer = Consumer("consumer1")
    consumer.init_consumer(interest, forwarder=forwarder1)
    provider = Provider("provider1")

    forwarder1.add_route(interest.name, forwarder2.node_info.name, forwarder2)
    forwarder2.add_route(interest.name, provider.name, provider)

    return [*consumer.get_tasks(), *forwarder1.get_tasks(), *forwarder2.get_tasks()]


async def main_test_2forwarders():
    """
                  Interest                Interest                 Interest
    ┌──────────┐ ─────────► ┌──────────┐ ─────────► ┌───────────┐ ─────────► ┌──────────┐
    │ Consumer │            │Forwarder1│            │ Forwarder2│            │ Provider │
    └──────────┘ ◄───────── └──────────┘ ◄───────── └───────────┘ ◄───────── └──────────┘
                    Data                    Data                     Data
    :return:
    """
    interest = Interest(
        name='/provider1/hello',
    )
    await asyncio.gather(*get_tasks2(interest))


if __name__ == '__main__':
    asyncio.run(main_test_2forwarders())
