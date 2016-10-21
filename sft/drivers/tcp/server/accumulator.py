"""
This module contains implementation of functionality for accumulating data and
data encapsulation in packets with fixed size.
"""

from sft.config import Config
from collections import defaultdict


_config = Config()


class Accumulator:

    def __init__(self):
        """ Initialize accumulator.
        """

        self._data_accumulators = defaultdict(bytearray)

    def accumulate_data(self, data):
        """
        Accumulate data.
        :param data: [(client_addr, raw_data), (client_addr, raw_data) ... ]
        :return ready_packages: packages that are ready for processing
                [(client_addr, pckt_payload), ... ]
        """

        ready_packages = []
        packet_size = _config.accumulator_packet_size

        for client_addr, data_chunk in data:
            self._data_accumulators[client_addr] += data_chunk

            if len(self._data_accumulators[client_addr]) >= packet_size:
                packet = self._data_accumulators[client_addr][:packet_size]
                ready_packages.append((client_addr, packet))
                self._data_accumulators[client_addr] = self._data_accumulators[client_addr][packet_size:]

        return ready_packages
