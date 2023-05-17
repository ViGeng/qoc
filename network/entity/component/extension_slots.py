# !/usr/bin/env python
# -*-coding:UTF-8 -*-

"""
# Time       : 2023/5/16 16:03
# Author     : Wei GENG
# Email      : rowan.gw@outlook.com
# Project    : named-tree 
# Description: 
"""
import asyncio

from network.entity.packet.data import Data


class ExtensionSlots:
    def __init__(self):
        self.extensions = []
        self.loop = asyncio.get_event_loop()

    def inbound_data_process(self, data) -> Data:
        for ext in self.extensions:
            data = ext.inbound_data_process(data)
            if data is None:
                return None
        return data

    def outbound_data_process(self, data) -> Data:
        for ext in self.extensions:
            data = ext.outbound_data_process(data)
            if data is None:
                return None
        return data

    async def inbound_interest_process(self, interest):
        for ext in self.extensions:
            interest = await ext.inbound_interest_process(interest)
            if interest is None:
                return None
        return interest

    def outbound_interest_process(self, interest):
        for ext in self.extensions:
            interest = ext.outbound_interest_process(interest)
            if interest is None:
                return None
        return interest

    def add_extension(self, extension):
        """
        Order matters
        :param extension:
        :return:
        """
        self.extensions.append(extension)
