from network.entity.packet.interest import Interest
from network.node_factory import NodeFactory
from network.route import Route


class RouteFactory:
    _instance = None

    @staticmethod
    def init(routes: dict, nodes: list[str]):
        node_factory = NodeFactory()
        node_dict = {}
        for node_name in nodes:
            node_dict[node_name] = node_factory.generate_instance_by_name(node_name)
        RouteFactory._instance = Route(routes, node_dict)

    @staticmethod
    def get_route():
        if RouteFactory._instance is None:
            raise ValueError("Route is not initialized")
        return RouteFactory._instance

    @staticmethod
    def set_interest(interest_configs: dict, route: Route):
        for consumer_name, interest_config in interest_configs.items():
            consumer = route.node(consumer_name)
            connected_fwd = route.node(interest_config[3])
            interest = Interest(interest_config[0], interest_config[1], interest_config[2])
            consumer.init_consumer(interest, connected_fwd, interest_config[4])
