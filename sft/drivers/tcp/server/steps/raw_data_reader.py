import logging
from sft.common.config import Config

import socket
from sft.common.sessions.session_manager import SessionManager
from sft.common.socket_manager import SocketManager


LOG = logging.getLogger(__name__)

_session_manager = SessionManager()
_socket_manager = SocketManager()
_buffer_size = Config().tcp_buffer_size


def _handle_client_disconnection(client_address):
    _session_manager.deactivate_session(client_address=client_address)
    _socket_manager.delete_socket_by_address(client_address)
    LOG.info('Client %s:%d: physical connection closed' % client_address)


def raw_data_reader(dummy_arg):
    """Receive data from tcp sockets.

       :param socket_list: List of sockets objects
       :return: [(client_address, data), (client_address, data), ...]
    """
    # LOG.debug('tcp raw_data_reader step')

    service_socket = _socket_manager.get_server_socket()
    sockets = _socket_manager.get_readable_sockets()
    raw_data = []

    for sock in sockets:
        if sock == service_socket:
            client_socket, client_address = service_socket.accept()
            _socket_manager.add_socket(client_socket, client_address)
            _session_manager.create_session(client_address)
            LOG.info('Client %s:%d: physical connection established' % client_address)
        else:
            client_address = sock.getpeername()
            try:
                data = sock.recv(_buffer_size)
                if data:
                    raw_data.append((client_address, data))
                else:
                    _handle_client_disconnection(client_address)
            except socket.error:
                _handle_client_disconnection(client_address)
                continue
    return raw_data
