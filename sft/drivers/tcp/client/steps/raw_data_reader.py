import logging
import socket

from sft.common.config import Config
from sft.common.socket_manager import SocketManager


LOG = logging.getLogger(__name__)

_socket_manager = SocketManager()
_buffer_size = Config().tcp_buffer_size


def _handle_server_disconnection():
    # Socket closed by server
    # ToDo: Ask user for trying reactivation
    raise Exception("Server socket closed")


def raw_data_reader(dummy_arg):
    """Receive data from tcp sockets.

       :param socket_list: List whith only one socket for reading data
       :return: [(server_addr, data), ]
    """
    LOG.debug('Client tcp raw_data_reader step')

    sockets = _socket_manager.get_readable_sockets()
    raw_data = []

    for sock in sockets:
        client_address = sock.getpeername()
        try:
            data = sock.recv(_buffer_size)
            if data:
                raw_data.append((client_address, data))
            else:
                _handle_server_disconnection()
        except socket.error:
            _handle_server_disconnection()
            continue
    return raw_data
