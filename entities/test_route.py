import asyncio

from entities.forwarder import Forwarder
from entities.packet import Interest
from entities.provider import Provider
from entities.route_factory import RouteFactory


async def test_route():
    """
                 C2
                 │
                 │
                 │
    C1────F4─────F1──────F2─────P1
                 │
                 │
                 F3
                 │
                 │
                 │
                 P2
    The above is the topology of this test
    C1 and C2 are consumers, send interest to P1 and P2 respectively
    F1, F2, F3, F4 are forwarders
    """
    routes = {
        '/p1/hello': {'f1': 'f2', 'f2': 'p1', 'f3': 'f1', 'f4': 'f1'},
        '/p2/hello': {'f1': 'f3', 'f2': 'f1', 'f3': 'p2', 'f4': 'f1'},
    }
    nodes = [
        'f1', 'f2', 'f3', 'f4',
        'p1', 'p2',
        'c1', 'c2'
    ]
    RouteFactory.init(routes, nodes)
    route = RouteFactory.get_route()

    route.node('c1').init_consumer(Interest('/p1/hello'), route.node('f4'))
    route.node('c2').init_consumer(Interest('/p2/hello'), route.node('f1'))

    # route.node('c2').is_enabled = False

    tasks = []
    for node_name, node in route.node_dict.items():
        if isinstance(node, Provider):
            continue
        if isinstance(node, Forwarder):
            node.set_route(route)
        tasks.extend(node.get_tasks())

    await asyncio.gather(*tasks)


def run():
    asyncio.run(test_route())


if __name__ == '__main__':
    run()
