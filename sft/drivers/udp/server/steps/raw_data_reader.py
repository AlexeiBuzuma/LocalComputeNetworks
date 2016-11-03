import logging
from sft.common.config import Config


LOG = logging.getLogger(__name__)

_config = Config()


def raw_data_reader(socket_list):
    """Receive data from udp sockets.

       :param socket_list: List of sockets objects
       :return: [(client_addr, data), (client_addr, data), ...]
    """
    LOG.debug('udp raw_data_reader step')
    buffer_size = _config.udp_buffer_size
    return [socket.recvfrom(buffer_size) for socket in socket_list]
