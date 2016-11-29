import logging

from sft.common.sessions.session_manager import SessionManager
from sft.common.socket_manager import SocketManager


LOG = logging.getLogger(__name__)

_session_manager = SessionManager()
_socket_manager = SocketManager()


def payload_collector(dummy_arg):
    # LOG.debug('std payload_collector step')
    data = []
    for socket in _socket_manager.get_writable_sockets():
        session = _session_manager.get_session_by_address(socket.getpeername(), create_new=True)
        command_data = session.command_generate_data()
        if command_data is not None:
            data.append((session.client_address, command_data))
    return data
