""" This module contains functionality for RawDataNormalizer.
"""

import abc


class DataNormalizer(metaclass=abc.ABCMeta):
    def __init__(self, acсumulator):
        self._accumulator = acсumulator

    @abc.abstractmethod
    def normalize(self, data):
        pass


class TCPNormalizer(DataNormalizer):
    """ Send all data into accumulator.
    """

    def normalize(self, data):
        self._accumulator.accumulate_data(data)


class UDPNormalizer(DataNormalizer):

    def normalize(self, data):
        # ToDo: Should contains functionality for QoS.

        raise NotImplementedError()
