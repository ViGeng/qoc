# !/usr/bin/env python
# -*-coding:UTF-8 -*-

"""
# Time       : 2023/5/16 16:36
# Author     : Wei GENG
# Email      : rowan.gw@outlook.com
# Project    : named-tree 
# Description: 
"""
from network.entity.extension.abstract_extension import AbstractExtension
from network.entity.packet.data import Data
from network.entity.packet.interest import Interest


class StatisticsExtension(AbstractExtension):
    def __init__(self):
        super().__init__()
        self._inbound_interest_count = 0
        self._outbound_interest_count = 0
        self._inbound_data_count = 0
        self._outbound_data_count = 0

    def inbound_interest_process(self, interest) -> Interest:
        self._inbound_interest_count += 1
        return interest

    def outbound_interest_process(self, interest) -> Interest:
        self._outbound_interest_count += 1
        return interest

    def inbound_data_process(self, data) -> Data:
        self._inbound_data_count += 1
        return data

    def outbound_data_process(self, data) -> Data:
        self._outbound_data_count += 1
        return data

    def statistics(self):
        return {
            "inbound_interest_count": self._inbound_interest_count,
            "outbound_interest_count": self._outbound_interest_count,
            "inbound_data_count": self._inbound_data_count,
            "outbound_data_count": self._outbound_data_count,
        }
