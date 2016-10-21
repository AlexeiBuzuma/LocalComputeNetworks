"""Module сontains all server basic execution steps.
   Each step in dict must be a tuple of callables.
   Each step can be overloaded in driver steps dict.
"""

import abc
import logging
from sft.server.sessions.session_manager import SessionManager
from sft.utils.packets import get_command_id
from sft.server.commands.base import HEARTBIT_COMMAND_ID


LOG = logging.getLogger(__name__)
_session_manager = SessionManager()


# ------------------ TimestampUpdaterStep ------------------
# Functions in this step shouldn't change the data, just skip data through itself.

def recv_timestamp_updater(data):
    """ Update last receive time for all clients, from which received data.
    """
    LOG.debug('Receive timestamp updater step')

    for client_addr, _ in data:
        session = _session_manager.get_session_by_address(client_addr, create_new=False)
        if session is not None:
            session.update_recv_time()

    return data


def sent_timestamp_updater(data):
    """ Update last sent time for all clients, for which was sent data.
    """
    LOG.debug('Sent timestamp updater step')

    for client_addr, _ in data:
        session = _session_manager.get_session_by_address(client_addr, create_new=False)
        if session is not None:
            session.update_sent_time()

    return data

# ----------------------------------------------------------


# ------------------ RawDataNormalizerStep ------------------

class DataNormalizer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def normalize(self, data):
        pass

# -----------------------------------------------------------


# ------------------ HeartbitReceiverStep ------------------

def heartbit_filter(data):
    """
    Filter Heartbit packages from data flow.
    :param data:
    :return:
    """
    LOG.debug('Heartbit Receiver Step')
    return list(filter(lambda x: get_command_id(x[1]) != HEARTBIT_COMMAND_ID, data))

# ----------------------------------------------------------



steps = {
    'socket_selector': (lambda x: LOG.debug('socket_selection_step'), ),
    'raw_data_reader': (lambda x: LOG.debug('raw_data_reader_step'), ),

    'lastrecv_timestamp_updater': (recv_timestamp_updater, ),
    'raw_data_normalizer': (lambda x: LOG.debug('raw_data_normalizer_step'), ),
    'heartbit_reciever': (heartbit_filter, ),
    'packet_dispatcher': (lambda x: LOG.debug('packet_dispatcher_step'), ),

    'packet_payload_collector': (lambda x: LOG.debug('packet_payload_collector_step'), ),
    'heartbit_sender': (lambda x: LOG.debug('heartbit_sender_step'), ),
    'lastsent_timestamp_updater': (sent_timestamp_updater, ),
    'packet_data_writer': (lambda x: LOG.debug('packet_data_writer_step'), ),

    'server_state_check': (lambda x: LOG.debug('server_state_check_step'), ),
}


