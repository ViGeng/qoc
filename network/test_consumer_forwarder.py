import asyncio

from network.entity.consumer import Consumer
from network.entity.forwarder import NodeInfo, Forwarder
from network.entity.packet import Interest, Data


def get_tasks(interest, data):
    node_info1 = NodeInfo(1, 'node1', 'node1')
    forwarder = Forwarder(node_info1)
    forwarder.cs.add(interest, data)

    consumer = Consumer("consumer1")
    consumer.init_consumer(interest, forwarder=forwarder)
    return consumer.get_tasks(), forwarder.get_tasks()


async def main_test_consumer2forwarder():
    """
                   Interest
     ┌──────────┬───────────►┌───────────┐
     │ Consumer │            │ Forwarder │
     └──────────┘◄───────────┴───────────┘
                     Data
    :return:
    """
    interest = Interest(
        name='/node1/hello',
    )
    data = Data(
        name="/node1/hello",
        data_content='hello world!',
    )
    cosumer_tasks, forwarder_tasks = get_tasks(interest, data)
    await asyncio.gather(*cosumer_tasks, *forwarder_tasks)


if __name__ == '__main__':
    asyncio.run(main_test_consumer2forwarder())

