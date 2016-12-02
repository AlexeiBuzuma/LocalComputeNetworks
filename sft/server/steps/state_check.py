import logging
import time

from sft.common.config import Config
from sft.common.sessions.session_manager import SessionManager


LOG = logging.getLogger(__name__)
_get_not_inactive_sessions = SessionManager().get_all_not_inactive_sessions
_deactivate_session = SessionManager().deactivate_session
_conn_break_timeout = Config().connection_break_timeout


def server_state_check(data):
    """Check last receive time in all active sessions.

       If time is expired, session will be deactivated.
    """
    active_sessions = _get_not_inactive_sessions()
    cur_time = time.time()

    for session in active_sessions:
        if cur_time - session.last_recv_time > _conn_break_timeout:
            _deactivate_session(session)
