""" This module contains functionality for TimestampUpdaterStep.
Functions in this step shouldn't change the data, just skip data through itself.
"""

from sft.session_manager import SessionManager

_session_manager = SessionManager()


def recv_timestamp_updater(data):
    """ Update last receive time for all clients, from which received data.
    """

    for client_addr, _ in data:
        session = _session_manager.get_session_by_address(client_addr, create_new=False)
        if session is not None:
            session.update_recv_time()

    return data


def sent_timestamp_updater(data):
    """ Update last sent time for all clients, for which was sent data.
    """

    for client_addr, _ in data:
        session = _session_manager.get_session_by_address(client_addr, create_new=False)
        if session is not None:
            session.update_sent_time()

    return data
