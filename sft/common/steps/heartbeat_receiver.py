import logging

from sft.common.commands.base import CommandIds
from sft.common.utils.packets import get_command_id
from sft.common.sessions.session_manager import SessionManager
from sft.common.config import Config

from time import time

LOG = logging.getLogger(__name__)
_session_manager = SessionManager()
_config = Config()
_heartbit_check_interval = _config.heartbeat_sender_interval - 3



def heartbeat_receiver(data):
    """Filter heartbeat packages from data flow.

       :param data: [(client_addr, pckt_payload), ... ]
       :return: [(client_addr, pckt_payload), ... ]
    """
    # LOG.debug('std heartbeat_receiver step')
    out_data = []

    for chunk in data:
        session = _session_manager.get_session(client_address=chunk[0])
        if time() - session.last_recv_time >= _heartbit_check_interval:
            if get_command_id(chunk[1]) != CommandIds.HEARTBEAT_COMMAND_ID:
                out_data.append(chunk)
        else:
            out_data.append(chunk)

        session = _session_manager.get_session(client_address=chunk[0], create_new=False)
        if session is not None:
            session.update_recv_time()

    return out_data
