import logging

from sft.common.steps.raw_data_normalizer import DataNormalizerBase


LOG = logging.getLogger(__name__)


class UDPNormalizer(DataNormalizerBase):
    def __init__(self):
        super().__init__()

        # ToDo: Create QoS object
        self._quality_of_service = object()

    def normalize(self, data):
        """
           :param data: [(client_addr, raw_data), ... ]
           :return: [(client_addr, pckt_payload), ... ]
        """
        # LOG.debug('udp raw_data_normalizer step')

        # ToDo: Should contain functionality for QoS.

        return data


raw_data_normalizer = UDPNormalizer().normalize
