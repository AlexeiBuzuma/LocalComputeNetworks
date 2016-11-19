import logging

from sft.common.sessions.session_manager import SessionManager


LOG = logging.getLogger(__name__)

_session_manager = SessionManager()


def lastrecv_timestamp_updater(data):
    """Update last_recv timestamp for the clients the data is from.

       Mustn't change the data, just pass it through.
    """
    LOG.debug('std lastrecv_timestamp_updater step')

    for client_addr, _ in data:
        session = _session_manager.get_session_by_address(
            client_addr, create_new=False)
        # if session is None:
        #     print("Session is None!")
        # else:
        #     print(session)
        if session is not None:
            session.update_recv_time()

    return data
