import logging
from sft.common.config import Config

from sft.common.sessions.session_manager import SessionManager
from sft.server.server import sockets


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

    for socket in data_socket:
        if socket == service_socket:
            client_socket, client_addr = service_socket.accept()
            sockets[client_addr] = client_socket
            _session_manager.create_session(client_addr)
            LOG.info('Physical connection with %s:%d was established' % client_addr)
        else:
            data = socket.recv(buffer_size)
            client_addr = socket.getpeername()

            if not data:
                _session_manager.deactivate_session_by_address(client_addr)
                sockets[client_addr].close()
                del sockets[client_addr]
                continue

            raw_data.append((client_addr, data))

    return raw_data
