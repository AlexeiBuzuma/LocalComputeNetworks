import logging

from sft.drivers.tcp.server.steps.socket_selector import socket_selector
from sft.drivers.tcp.server.steps.raw_data_reader import raw_data_reader
from sft.drivers.tcp.server.steps.raw_data_normalizer import raw_data_normalizer
from sft.drivers.tcp.server.steps.server_state_check import server_state_check
from sft.drivers.tcp.server.steps.packet_data_writer import packet_data_writer


LOG = logging.getLogger(__name__)


steps = {
    'socket_selector': (socket_selector, ),
    'raw_data_reader': (raw_data_reader, ),
    'raw_data_normalizer': (raw_data_normalizer, ),
    'packet_data_writer': (packet_data_writer, ),
    'server_state_check': (server_state_check, ),
}
