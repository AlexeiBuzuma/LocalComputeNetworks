import logging

from sft.common.sessions.session_manager import SessionManager


LOG = logging.getLogger(__name__)

_session_manager = SessionManager()


def lastsent_timestamp_updater(data):
    """Update last_sent timestamp for the clients the data is for.

       Mustn't change the data, just pass it through.
    """
    # LOG.debug('std lastsent_timestamp_updater step')

    for client_addr, _ in data:
        session = _session_manager.get_session(client_address=client_addr, create_new=False)
        if session is not None:
            session.update_sent_time()

    return data
