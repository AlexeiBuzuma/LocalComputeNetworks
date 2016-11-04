import logging


LOG = logging.getLogger(__name__)


def get_command_id(packet_payload):
    return int.from_bytes(packet_payload[0:1], 'big')


def get_heartbeat_payload():
    # ToDo: add heartbeat packet payload
    return b'\x00' * 7
