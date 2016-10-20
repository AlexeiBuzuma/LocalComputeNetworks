import logging


LOG = logging.getLogger(__name__)


steps = {
    'socket_selector': (
        lambda x: LOG.debug('socket_selection_step'), ),

    'raw_data_reader': (
        lambda x: LOG.debug('raw_data_reader_step'), ),
    'lastrecv_timestamp_updater': (
        lambda x: LOG.debug('lastrecv_timestamp_updater_step'), ),
    'raw_data_normalizer': (
        lambda x: LOG.debug('raw_data_normalizer_step'), ),
    'heartbit_reciever': (
        lambda x: LOG.debug('heartbit_reciever_step'), ),
    'packet_dispatcher': (
        lambda x: LOG.debug('packet_dispatcher_step'), ),

    'packet_payload_collector': (
        lambda x: LOG.debug('packet_payload_collector_step'), ),
    'heartbit_sender': (
        lambda x: LOG.debug('heartbit_sender_step'), ),
    'lastsent_timestamp_updater': (
        lambda x: LOG.debug('lastsent_timestamp_updater_step'), ),
    'packet_data_writer': (
        lambda x: LOG.debug('packet_data_writer_step'), ),

    'server_state_check': (
        lambda x: LOG.debug('server_state_check_step'), ),
}
