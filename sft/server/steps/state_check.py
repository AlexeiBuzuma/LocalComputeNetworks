import logging
import time

from sft.common.config import Config
from sft.common.sessions.session_manager import SessionManager, SessionStatus

LOG = logging.getLogger(__name__)
_config = Config()


def server_state_check(data):
    """ Check last receive time in all active sessions. If time is expired, session will be deactivated.
    """

    LOG.debug("Server state check")

    session_manager = SessionManager()
    active_sessions = session_manager.get_all_not_inactive_sessions()

    for session in active_sessions:
        sec_from_last_recv = time.time() - session.last_recv_time
        if sec_from_last_recv > _config.connection_break_timeout:
            session.status = SessionStatus.inactive
