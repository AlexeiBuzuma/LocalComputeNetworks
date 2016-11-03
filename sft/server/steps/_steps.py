"""Module сontains all server execution steps.
   Each step in dict must be a tuple of callables.
   Each step can be overloaded in driver steps dict.
"""

import logging

from sft.server.steps.socket_selector import socket_selector
from sft.server.steps.lastrecv_updater import lastrecv_timestamp_updater
from sft.server.steps.raw_data_normalizer import raw_data_normalizer
from sft.server.steps.heartbit_reciever import heartbit_reciever
from sft.server.steps.packet_dispatcher import packet_dispatcher

from sft.server.steps.payload_collector import payload_collector
from sft.server.steps.heartbit_sender import heartbit_sender
from sft.server.steps.lastsent_updater import lastsent_timestamp_updater


LOG = logging.getLogger(__name__)


steps = {
    'socket_selector': (socket_selector, ),

    'raw_data_reader': (lambda x: LOG.debug('std raw_data_reader step'), ),
    'lastrecv_timestamp_updater': (lastrecv_timestamp_updater, ),
    'raw_data_normalizer': (raw_data_normalizer, ),
    'heartbit_reciever': (heartbit_reciever, ),
    'packet_dispatcher': (packet_dispatcher, ),

    'payload_collector': (payload_collector, ),
    'heartbit_sender': (heartbit_sender, ),
    'lastsent_timestamp_updater': (lastsent_timestamp_updater, ),
    'packet_data_writer': (lambda x: LOG.debug('std packet_data_writer step'), ),

    'server_state_check': (lambda x: LOG.debug('std server_state_check step'), ),
}
