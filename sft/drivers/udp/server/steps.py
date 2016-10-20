import logging
from sft.config import Config
from sft.server.steps.default import DataNormalizer


LOG = logging.getLogger(__name__)
_config = Config()


# ------------------ DataReadingStep ------------------

def raw_data_udp_reader(socket_list):
    """
    Receive data from udp sockets.
    :param socket_list: List of sockets objects
    :return: [(client_addr, data), (client_addr, data), ...]
    """

    buffer_size = _config.udp_buffer_size
    return [socket.recvfrom(buffer_size) for socket in socket_list]

# -----------------------------------------------------


# ------------------ RawDataNormalizerStep ------------------

class UDPNormalizer(DataNormalizer):

    def __init__(self, quality_of_service):
        super().__init__()
        self._quality_of_service = quality_of_service

    def normalize(self, data):
        # ToDo: Should contains functionality for QoS.

        raise NotImplementedError()

# -----------------------------------------------------------


steps = {
    'raw_data_reader': (raw_data_udp_reader, ),
    'raw_data_normalizer': (lambda x: LOG.debug('udp_qos_step'), ),

    'packet_data_writer': (lambda x: LOG.debug('udp_data_writer_step'), ),

    'server_state_check': (lambda x: LOG.debug('udp_server_state_check_step'), ),
}
