# !/usr/bin/env python
# -*-coding:UTF-8 -*-

"""
# Time       : 2023/5/16 16:03
# Author     : Wei GENG
# Email      : rowan.gw@outlook.com
# Project    : named-tree 
# Description: 
"""
from network.entity.packet.data import Data


class ExtensionSlots:
    def __init__(self):
        self.extensions = []

    def inbound_data_process(self, data) -> Data:
        for ext in self.extensions:
            data = ext.inbound_data_process(data)
        return data

    def outbound_data_process(self, data) -> Data:
        for ext in self.extensions:
            data = ext.outbound_data_process(data)
        return data

    def inbound_interest_process(self, interest):
        for ext in self.extensions:
            interest = ext.inbound_interest_process(interest)
        return interest

    def outbound_interest_process(self, interest):
        for ext in self.extensions:
            interest = ext.outbound_interest_process(interest)
        return interest

    def add_extension(self, extension):
        """
        Order matters
        :param extension:
        :return:
        """
        self.extensions.append(extension)
