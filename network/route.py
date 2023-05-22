from network.node_factory import NodeFactory


class Route:
    def __init__(self, routes: dict, node_dict: dict):
        self.routes = routes
        self.node_dict = node_dict

    def query_route(self, interest_name: str, self_node_name: str):
        next_hop_name = self.routes[interest_name][self_node_name]
        return self.node_dict[next_hop_name]

    def node(self, node_name: str):
        return self.node_dict[node_name]
