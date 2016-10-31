import logging
from sft.config import Config

from sft.server.sessions.session_manager import SessionManager
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

    service_socket = sockets["service_socket"]
    buffer_size = _config.tcp_buffer_size

    raw_data = []

    for socket in socket_list:
        if socket == service_socket:
            client_socket, client_addr = service_socket.accept()
            socket[client_addr] = client_socket
            _session_manager.create_session(client_addr)
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
