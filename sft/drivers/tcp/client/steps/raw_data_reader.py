import logging
import socket

from sft.common.commands.base import ErrorIds, ProgramFinished
from sft.common.config import Config
from sft.common.socket_manager import SocketManager
from sft.common.sessions.session_manager import SessionManager, SessionStatus


LOG = logging.getLogger(__name__)

_socket_manager = SocketManager()
_buffer_size = Config().tcp_buffer_size


def _handle_server_disconnection():
    # Socket closed by server
    # ToDo: Ask user for trying reactivation
    session = SessionManager().get_all_not_inactive_sessions()[0]
    if session.status == SessionStatus.wait_for_close:
        raise ProgramFinished(ErrorIds.SUCCESSFUL)
    raise Exception("Server socket closed unexpectedly")


def raw_data_reader(dummy_arg):
    """Receive data from tcp sockets.

       :param socket_list: List whith only one socket for reading data
       :return: [(server_addr, data), ]
    """

    sockets = _socket_manager.readable
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
