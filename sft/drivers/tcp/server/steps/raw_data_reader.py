import logging
from sft.common.config import Config

import socket
from sft.common.sessions.session_manager import SessionManager
from sft.server.server import sockets



LOG = logging.getLogger(__name__)

_config = Config()
_session_manager = SessionManager()


def _handle_client_disconnection(client_address):
    _session_manager.deactivate_session_by_address(client_address)
    sockets[client_address].close()
    del sockets[client_address]
    LOG.info('Client %s:%d: disconnected' % client_address)


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

    for sock in data_socket:
        if sock == service_socket:
            client_socket, client_addr = service_socket.accept()
            sockets[client_addr] = client_socket
            _session_manager.create_session(client_addr)
            LOG.info('Client %s:%d: physical connection established' % client_addr)
        else:
            client_addr = sock.getpeername()
            try:
                data = sock.recv(buffer_size)
                if data:
                    raw_data.append((client_addr, data))
                else:
                    _handle_client_disconnection(client_addr)
            except socket.error:
                _handle_client_disconnection(client_addr)
                continue
    return raw_data
