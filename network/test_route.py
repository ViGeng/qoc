import asyncio

from network.entity.forwarder import Forwarder
from network.entity.packet.interest import Interest
from network.entity.provider import Provider
from network.route_factory import RouteFactory


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
    eg:
    f1-cs-nf is a forwarder with cs and nfn extension
    """
    routes = {
        '/p1/hello': {'f1-cs-nf': 'f2cs', 'f2cs': 'p1', 'f3cs': 'f1-cs-nf', 'f4cs': 'f1-cs-nf'},
        '/p1/nfn': {'f1-cs-nf': 'f2cs', 'f2cs': 'p1', 'f3cs': 'f1-cs-nf', 'f4cs': 'f1-cs-nf'},
        '/p2/hello': {'f1-cs-nf': 'f3cs', 'f2cs': 'f1', 'f3cs': 'p2', 'f4cs': 'f1-cs-nf'},
    }
    nodes = [
        'f1-cs-nf', 'f2cs', 'f3cs', 'f4cs',
        'p1', 'p2',
        'c1', 'c2'
    ]
    RouteFactory.init(routes, nodes)
    route = RouteFactory.get_route()

    nf_interest = Interest('/p1/nfn', data_name=1, func=lambda x: x+1)  # TODO: here we use the simplest function

    route.node('c1').init_consumer(nf_interest, route.node('f4cs'))
    route.node('c2').init_consumer(Interest('/p2/hello'), route.node('f1-cs-nf'))

    route.node('c2').is_enabled = False

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
