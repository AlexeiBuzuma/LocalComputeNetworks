import logging
import time

from sft.common.commands.base import ProgramFinished, ErrorIds
from sft.common.config import Config
from sft.common.sessions.session_manager import SessionManager
from sft.common.socket_manager import SocketManager

LOG = logging.getLogger(__name__)
_get_not_inactive_sessions = SessionManager().get_all_not_inactive_sessions
_deactivate_session = SessionManager().deactivate_session
_conn_break_timeout = Config().connection_break_timeout


def client_state_check(data):
    # ToDo: Do sth with exceptional sockets
    active_sessions = _get_not_inactive_sessions()
    cur_time = time.time()

    for session in active_sessions:
        if cur_time - session.last_recv_time > _conn_break_timeout:
            LOG.warning("Server %s:%d: seems that physical connection is broken" % session.client_address)
            _deactivate_session(session)
            raise ProgramFinished(ErrorIds.ERROR)
