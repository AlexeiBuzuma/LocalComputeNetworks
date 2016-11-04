import logging
import select

LOG = logging.getLogger(__name__)


def socket_selector(data):
    """Universal socket selection step.

       :param data: (service_socket, [data_socket, data_socket, ...])
       :return: (readable, writable, exceptional)
    """
    LOG.debug('socket_selection step.')
    service_socket, data_sockets = data
    LOG.debug('Sockets in selection step: %r' % data_sockets)
    readable, writable, exceptional = select.select(data_sockets, data_sockets, data_sockets, 0.05)
    LOG.debug('R: %r' % readable)
    LOG.debug('W: %r' % writable)
    LOG.debug('E: %r' % exceptional)

    return readable, writable, exceptional
