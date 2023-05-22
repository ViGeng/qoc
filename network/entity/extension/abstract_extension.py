# !/usr/bin/env python
# -*-coding:UTF-8 -*-

"""
# Time       : 2023/5/16 15:52
# Author     : Wei GENG
# Email      : rowan.gw@outlook.com
# Project    : named-tree 
# Description: 
"""
from abc import abstractmethod

from network.entity.packet.data import Data
from network.entity.packet.interest import Interest


class AbstractExtension:
    @abstractmethod
    def inbound_data_process(self, data) -> Data:
        pass

    @abstractmethod
    def outbound_data_process(self, data) -> Data:
        pass

    @abstractmethod
    def inbound_interest_process(self, interest) -> Interest:
        pass

    @abstractmethod
    def outbound_interest_process(self, interest) -> Interest:
        pass
