import logging

from sft.common.steps.raw_data_normalizer import DataNormalizerBase
from sft.drivers.tcp.server.accumulator import Accumulator


LOG = logging.getLogger(__name__)


class TCPNormalizer(DataNormalizerBase):
    """Send all data into accumulator."""
    def __init__(self):
        super().__init__()
        self._accumulator = Accumulator()

    def normalize(self, data):
        """
           :param data: [(server_addr, raw_data), ]
           :return: [(server_addr, pckt_payload), ]
        """
        # LOG.debug('Client tcp raw_data_normalizer step')
        return self._accumulator.accumulate_data(data)


raw_data_normalizer = TCPNormalizer().normalize
