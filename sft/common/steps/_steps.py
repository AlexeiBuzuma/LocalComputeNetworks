"""Module сontains all server execution steps.
   Each step in dict must be a tuple of callables.
   Each step can be overloaded in driver steps dict.
"""

import logging

from sft.common.steps.socket_selector import socket_selector
from sft.common.steps.lastrecv_updater import lastrecv_timestamp_updater
from sft.common.steps.raw_data_normalizer import raw_data_normalizer
from sft.common.steps.heartbeat_receiver import heartbeat_receiver
from sft.common.steps.packet_dispatcher import packet_dispatcher

from sft.common.steps.payload_collector import payload_collector
from sft.common.steps.lastsent_updater import lastsent_timestamp_updater


LOG = logging.getLogger(__name__)


steps = {
    'socket_selector': (socket_selector, ),

    'raw_data_reader': (lambda x: LOG.debug('std raw_data_reader step'), ),
    'lastrecv_timestamp_updater': (lastrecv_timestamp_updater, ),
    'raw_data_normalizer': (raw_data_normalizer, ),
    'heartbeat_receiver': (heartbeat_receiver, ),
    'packet_dispatcher': (packet_dispatcher, ),

    'payload_collector': (payload_collector, ),
    'lastsent_timestamp_updater': (lastsent_timestamp_updater, ),
    'packet_data_writer': (lambda x: LOG.debug('std packet_data_writer step'), ),

    'state_check': (lambda x: LOG.debug('std state_check step'), ),
}
