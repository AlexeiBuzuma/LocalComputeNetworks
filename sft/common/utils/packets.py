import logging
from sft.common.config import Config
from sft.common.commands.base import CommandIds


LOG = logging.getLogger(__name__)
_config = Config()

#
# | command_id | error_code | payload_size | .... payload .... |
# 0            1            2              6                   ?

# For performance optimization
_command_id_size = _config.command_id_size
_error_code_size = _config.error_code_size
_payload_size = _config.payload_size
_packet_size = _config.package_size
_header_size = _command_id_size + _error_code_size + _payload_size
_packet_with_header_payload_size = _packet_size - _header_size



def get_command_id(packet_payload):
    return int.from_bytes(packet_payload[0:_command_id_size], 'big')


def get_error_code(packet_payload):
    start_index = _command_id_size
    return int.from_bytes(packet_payload[start_index:start_index+_error_code_size], 'big')


def get_payload_size(packet_payload):
    start_index = _command_id_size + _error_code_size
    return int.from_bytes(packet_payload[start_index:start_index + _payload_size], 'big')


def get_payload(packet_payload):
    start_index = _command_id_size + _error_code_size + _payload_size
    return packet_payload[start_index:start_index+get_payload_size(packet_payload)].decode("utf-8")


def get_payload_bytes(packet_payload):
    start_index = _command_id_size + _error_code_size + _payload_size
    return packet_payload[start_index:start_index+get_payload_size(packet_payload)]


def get_payload_by_size(packet_payload, size):
    start_index = _command_id_size + _error_code_size + _payload_size
    return packet_payload[start_index:start_index+size]


def generate_header(command_id, error_code, payload_size):
    header = int.to_bytes(command_id, _command_id_size, "big")
    header += int.to_bytes(error_code, _error_code_size, "big")
    header += int.to_bytes(payload_size, _payload_size, "big")

    return header


def get_header_size():
    return _header_size


def get_packet_with_header_payload_size():
    return _packet_with_header_payload_size


def generate_packet(command_id, error_code, data):
    """ Generate packet for single-packet command.
    """

    data_bytes = bytearray(data, "utf-8")
    header = generate_header(command_id, error_code, len(data_bytes))
    packet = header + data_bytes
    packet = packet + bytes(_config.package_size - len(packet))
    return packet


def get_heartbeat_payload():
    return generate_packet(CommandIds.HEARTBEAT_COMMAND_ID.value, 0, "")
