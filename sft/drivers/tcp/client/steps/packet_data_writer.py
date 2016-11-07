import logging

from sft.client.client import sockets


LOG = logging.getLogger(__name__)


def packet_data_writer(packet_payloads):
    LOG.debug('tcp packet_data_writer step')
    for address, payload in packet_payloads:
        sockets[address].send(payload)
