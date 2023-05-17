import asyncio
import os
from unittest import TestCase

import yaml

from network.simulator import Simulator


async def main():
    route_config, node_config, interest_config = load_config_from_path('config_files/case1.yaml')
    simulator = Simulator(route_config, node_config, interest_config)
    await asyncio.gather(*simulator.get_task())


# load config from path, return route_config, node_config, interest_config
def load_config_from_path(path):
    # determine the path exists
    if not os.path.exists(path):
        raise ValueError(f"Path {path} not exists")
    # determine the path is a file
    if not os.path.isfile(path):
        raise ValueError(f"Path {path} is not a file")
    with open(path, 'r') as f:
        config = yaml.safe_load(f)

    route_config = config.get('route_config', {})
    node_config = config.get('node_config', [])
    interest_config = config.get('interest_config', {})
    return route_config, node_config, interest_config


class Test(TestCase):
    def test_simulator_1(self):
        asyncio.run(main())
