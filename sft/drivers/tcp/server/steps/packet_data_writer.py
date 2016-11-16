import logging

from sft.common.socket_manager import SocketManager


LOG = logging.getLogger(__name__)

_sock_manager = SocketManager()


def packet_data_writer(packet_payloads):
    LOG.debug('tcp packet_data_writer step')
    print("Number of packets to write: {0}".format(len(packet_payloads)))
    for address, payload in packet_payloads:
        _sock_manager.get_socket_by_address(address).send(payload)
