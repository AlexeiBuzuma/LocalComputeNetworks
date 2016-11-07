import logging

from sft.common.socket_manager import SocketManager


LOG = logging.getLogger(__name__)

_sock_manager = SocketManager()


def packet_data_writer(packet_payloads):
    LOG.debug('tcp packet_data_writer step')
    for address, payload in packet_payloads:
        _sock_manager.get_socket_by_address(address).send(payload)
