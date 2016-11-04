import logging

from sft.common.sessions.session_manager import SessionManager


LOG = logging.getLogger(__name__)

_session_manager = SessionManager()


def payload_collector(writable_sockets):
    LOG.debug('std payload_collector step')
    data = []
    for socket in writable_sockets:
        session = _session_manager.get_session_by_address(socket.getpeername(), create_new=False)
        command_data = session.command_generate_data()
        if command_data is not None:
            data.append((session.client_address, command_data))
    return data
