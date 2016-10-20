import logging


LOG = logging.getLogger(__name__)


steps = {
    'raw_data_reader': (
        lambda x: LOG.debug('udp_raw_data_reader_step'), ),
    'raw_data_normalizer': (
        lambda x: LOG.debug('udp_qos_step'), ),

    'packet_data_writer': (
        lambda x: LOG.debug('udp_data_writer_step'), ),

    'server_state_check': (
        lambda x: LOG.debug('udp_server_state_check_step'), ),
}
