import logging
from sft.common.config import Config

from sft.common.sessions.session_manager import SessionManager
from sft.client.client import sockets


LOG = logging.getLogger(__name__)

_config = Config()
_session_manager = SessionManager()


def raw_data_reader(socket_list):
    """Receive data from tcp sockets.

       :param socket_list: List of sockets objects
       :return: [(client_addr, data), (client_addr, data), ...]
    """
    LOG.debug('tcp raw_data_reader step')
    LOG.debug("socket_list: {}".format(socket_list))
    service_socket, data_socket = socket_list
    buffer_size = _config.tcp_buffer_size

    raw_data = []

    return raw_data
