import logging
import time

from sft.common.config import Config
from sft.common.sessions.session_manager import SessionManager, SessionStatus

LOG = logging.getLogger(__name__)
_config = Config()


def state_check():
    """ Check last receive time in all active sessions. If time is expired, session will be deactivated.
    """

    session_manager = SessionManager()
    active_sessions = session_manager.get_all_active_sessions()

    for session in active_sessions:
        sec_from_last_recv = time.time() - session.last_recv_time
        if sec_from_last_recv > _config.connection_break_timeout:
            session.status = SessionStatus.inactive
