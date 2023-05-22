import asyncio

from network.entity.forwarder import Forwarder
from network.entity.provider import Provider
from network.route_factory import RouteFactory


class Simulator:
    def __init__(self, route_config, node_config, interest_config):
        RouteFactory.init(route_config, node_config)
        self.route = RouteFactory.get_route()
        self.interest_config = interest_config
        RouteFactory.set_interest(interest_config, self.route)
        self.tasks = []
        for node_name, node in self.route.node_dict.items():
            if isinstance(node, Provider):
                continue
            if isinstance(node, Forwarder):
                node.set_route(self.route)
            self.tasks.extend(node.get_tasks())

    def get_task(self):
        return self.tasks



