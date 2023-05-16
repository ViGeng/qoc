# !/usr/bin/env python
# -*-coding:UTF-8 -*-

"""
# Time       : 2023/5/16 15:58
# Author     : Wei GENG
# Email      : rowan.gw@outlook.com
# Project    : named-tree 
# Description: 
"""
from logging import debug

from network.entity.extension.abstract_extension import AbstractExtension
from network.entity.packet.data import Data
from network.entity.packet.interest import Interest


class HelloExtension(AbstractExtension):

    def inbound_data_process(self, data) -> Data:
        debug(f"HelloExtension: inbound_data_process {data}")
        return data

    def outbound_data_process(self, data) -> Data:
        debug(f"HelloExtension: outbound_data_process {data}")
        return data

    def outbound_interest_process(self, interest) -> Interest:
        debug(f"HelloExtension: outbound_interest_process {interest}")
        return interest

    def inbound_interest_process(self, interest) -> Interest:
        debug(f"HelloExtension: inbound_interest_process {interest}")
        return interest
