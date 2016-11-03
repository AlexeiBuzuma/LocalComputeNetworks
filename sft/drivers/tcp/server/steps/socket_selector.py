import logging
import select

LOG = logging.getLogger(__name__)


def socket_selector(data):
    """
        Specific socket selection step for tcp mode.
       :param data: (service_socket, [data_socket, data_socket, ...])
       :return: (readable, writable, exceptional)
    """
    LOG.debug('socket_selection step.')
    service_socket, data_sockets = data
    readable, writable, exceptional = select.select(data_sockets, data_sockets, data_sockets)

    return readable, writable, exceptional
