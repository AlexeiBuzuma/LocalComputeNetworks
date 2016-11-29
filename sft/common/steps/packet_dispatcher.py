import logging

from sft.common.sessions.session_manager import SessionManager


LOG = logging.getLogger(__name__)

_session_manager = SessionManager()


def packet_dispatcher(data):
    """Dispatch packets to appropriate sessions.

       :param data: [(client_addr, packet_payload), ...]
       :return []
    """
    # LOG.debug('std packet_dispatcher step')

    for client__address, data in data:
        session = _session_manager.get_session_by_address(client__address)
        session.command_receive_data(data)
