import logging
from sft.common.config import Config


LOG = logging.getLogger(__name__)
_config = Config()

#
# | packet_id | command_id | error_code | payload_size | .... payload .... |
# 0           2            3            4              9                   ?

# For performance optimization
_packet_id_size = _config.packet_id_size
_command_id_size = _config.command_id_size
_error_code_size = _config.error_code_size
_payload_size = _config.payload_size


def get_packet_id(packet_payload):
    return int.from_bytes(packet_payload[:_packet_id_size], 'big')


def get_command_id(packet_payload):
    return int.from_bytes(packet_payload[_packet_id_size:_command_id_size+_packet_id_size], 'big')


def get_error_code(packet_payload):
    start_index = _packet_id_size + _command_id_size
    return int.from_bytes(packet_payload[start_index:start_index+_error_code_size], 'big')


def get_payload_size(packet_payload):
    start_index = _packet_id_size + _command_id_size + _error_code_size
    return int.from_bytes(packet_payload[start_index:start_index + _payload_size], 'big')


def get_payload(packet_payload):
    start_index = _packet_id_size + _command_id_size + _error_code_size + _payload_size
    return packet_payload[start_index:start_index+_payload_size].decode("utf-8")


def generate_header(packet_id, command_id, error_code, payload_size):
    header = int.to_bytes(packet_id, _packet_id_size, "big")
    header += int.to_bytes(command_id, _command_id_size, "big")
    header += int.to_bytes(error_code, _error_code_size, "big")
    header += int.to_bytes(payload_size, _payload_size, "big")

    return header


def generate_packet(packet_id, command_id, error_code, data):
    data_bytes = bytearray(data, "utf-8")
    header = generate_header(packet_id, command_id, error_code, len(data_bytes))
    return data_bytes + header


def get_heartbeat_payload():
    # ToDo: add heartbeat packet payload
    return b'\x00' * 7
