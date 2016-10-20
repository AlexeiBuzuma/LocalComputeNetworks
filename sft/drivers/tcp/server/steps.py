import logging
from sft.config import Config
from sft.server.sessions.session_manager import SessionManager
from sft.server.steps.default import DataNormalizer


LOG = logging.getLogger(__name__)
_config = Config()
_session_manager = SessionManager()


# ------------------ DataReadingStep ------------------

def raw_data_tcp_reader(socket_list):
    """
    Receive data from tcp sockets.
    :param socket_list: List of sockets objects
    :return: [(client_addr, data), (client_addr, data), ...]
    """

    buffer_size = _config.tcp_buffer_size

    raw_data = []

    for socket in socket_list:
        data = socket.recv(buffer_size)
        client_addr = socket.getpeername()

        if not data:
            _session_manager.deactivate_session_by_address(client_addr)
            # ToDo: Close socket in SocketContainer
            continue

        raw_data.append((client_addr, data))

    return raw_data

# -----------------------------------------------------


# ------------------ RawDataNormalizerStep ------------------

# ToDo: How to set this step in the dict, if we need in initialized accumulator for create normalizer?
class TCPNormalizer(DataNormalizer):
    """ Send all data into accumulator.
    """

    def __init__(self, accumulator):
        super().__init__()
        self._accumulator = accumulator

    def normalize(self, data):
        self._accumulator.accumulate_data(data)

# -----------------------------------------------------------


steps = {
    'raw_data_reader': (raw_data_tcp_reader, ),
    'raw_data_normalizer': (lambda x: LOG.debug('tcp_data_accumulating_step'), ),

    'packet_data_writer': (lambda x: LOG.debug('tcp_data_writer_step'), ),

    'server_state_check': (lambda x: LOG.debug('tcp_server_state_check_step'), ),
}
