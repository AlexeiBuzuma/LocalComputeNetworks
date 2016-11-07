import logging

from .raw_data_reader import raw_data_reader
from .raw_data_normalizer import raw_data_normalizer
from .packet_data_writer import packet_data_writer
from .state_check import state_check


LOG = logging.getLogger(__name__)


steps = {
    'raw_data_reader': (raw_data_reader, ),
    'raw_data_normalizer': (raw_data_normalizer, ),
    'packet_data_writer': (packet_data_writer, ),
    'state_check': (state_check, ),
}
