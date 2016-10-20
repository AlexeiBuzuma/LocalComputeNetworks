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

        self._handlers = []
        self._data_accumulators = defaultdict(bytearray)

    def accumulate_data_chunk(self, initiator, data):
        """
        Accumulate data chunk.
        :param initiator: Client address
        :param data: data for accumulate
        """

        self._data_accumulators[initiator] += data
        packet_size = _config.accumulator_packet_size

        if len(self._data_accumulators[initiator]) >= packet_size:
            packet = self._data_accumulators[initiator][:packet_size]

            for handler in self._handlers:
                handler(initiator, packet)

            self._data_accumulators[initiator] = self._data_accumulators[initiator][packet_size:]

    def accumulate_data(self, data):
        """
        Accumulate data.
        :param data: [(cliend_addr, data), (client_addr, data) ... ]
        """

        for client_addr, data in data:
            self.accumulate_data_chunk(client_addr, data)

    def add_handler(self, handler):
        """ Add event handler to accumulator.

        Handler will be called, when packet will be formatted.
        In the handler will be sent info about client address and packet data.initiator
        Info about packet will be removed after execution of the handlers
        """

        if not callable(handler):
            raise AttributeError("Handler mast be a callable object.")

        if handler in self._handlers:
            raise AttributeError("Handler {} already subscribed".format(repr(handler)))

        self._handlers.append(handler)

if __name__ == '__main__':
    """ Example is using accumulator.
    """

    import os

    def handler(initiator, data):
        print("Process data from initiator: {}".format(initiator))
        print("Data: {} ... {}".format(data[:10], data[-10:]))
        print("------------------------------------------")


    packet_size = _config.accumulator_packet_size
    print("Packet size: {}\n\n".format(packet_size))

    accumulator = Accumulator()
    accumulator.add_handler(handler)

    accumulator.accumulate_data_chunk("Initiator1", os.urandom(int(packet_size * 0.66)))
    accumulator.accumulate_data_chunk("Initiator2", os.urandom(int(packet_size * 0.66)))
    accumulator.accumulate_data_chunk("Initiator3", os.urandom(int(packet_size * 0.66)))

    for acc in accumulator._data_accumulators:
        print("{} --> Len: {}".format(acc, len(accumulator._data_accumulators.get(acc))))
    print("----------------------------------------------------------------------------\n")

    accumulator.accumulate_data_chunk("Initiator1", os.urandom(int(packet_size * 0.12)))
    accumulator.accumulate_data_chunk("Initiator2", os.urandom(int(packet_size * 0.12)))
    accumulator.accumulate_data_chunk("Initiator3", os.urandom(int(packet_size * 0.12)))

    for acc in accumulator._data_accumulators:
        print("{} --> Len: {}".format(acc, len(accumulator._data_accumulators.get(acc))))
    print("----------------------------------------------------------------------------\n")

    accumulator.accumulate_data_chunk("Initiator3", os.urandom(int(packet_size * 0.66)))
    accumulator.accumulate_data_chunk("Initiator2", os.urandom(int(packet_size * 0.66)))
    accumulator.accumulate_data_chunk("Initiator1", os.urandom(int(packet_size * 0.66)))

    for acc in accumulator._data_accumulators:
        print("{}--> Len: {}".format(acc, len(accumulator._data_accumulators.get(acc))))
    print("----------------------------------------------------------------------------\n")

    accumulator.accumulate_data_chunk("Initiator1", os.urandom(int(packet_size * 0.66)))
    accumulator.accumulate_data_chunk("Initiator2", os.urandom(int(packet_size * 0.66)))
    accumulator.accumulate_data_chunk("Initiator3", os.urandom(int(packet_size * 0.66)))

    for acc in accumulator._data_accumulators:
        print("{}--> Len: {}".format(acc, len(accumulator._data_accumulators.get(acc))))
    print("----------------------------------------------------------------------------\n")
