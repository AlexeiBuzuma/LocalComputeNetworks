import logging

from sft.common.sessions.session_manager import SessionManager
from sft.common.socket_manager import SocketManager


LOG = logging.getLogger(__name__)

_get_session = SessionManager().get_session
_socket_manager = SocketManager()


def payload_collector(dummy_arg):
    data = []
    for socket in _socket_manager.writable:
        # ToDo: Rewrite payload collector to be appropriate for UDP
        # Slow for TCP and inappropriate for UDP
        # client_address = socket.getpeername()
        client_address = _socket_manager.address_by_socket_id[id(socket)]
        command_data = _get_session(client_address=client_address, create_new=True).command_generate_data()
        if command_data is not None:
            data.append((client_address, command_data))
    return data
