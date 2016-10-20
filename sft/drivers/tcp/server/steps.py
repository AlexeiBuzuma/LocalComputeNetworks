import logging


LOG = logging.getLogger(__name__)


steps = {
    'raw_data_reader': (
        lambda x: LOG.debug('tcp_raw_data_reader_step'), ),
    'raw_data_normalizer': (
        lambda x: LOG.debug('tcp_data_accumulating_step'), ),

    'packet_data_writer': (
        lambda x: LOG.debug('tcp_data_writer_step'), ),

    'server_state_check': (
        lambda x: LOG.debug('tcp_server_state_check_step'), ),
}
