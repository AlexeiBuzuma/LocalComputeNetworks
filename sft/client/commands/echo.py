import logging

from sft.common.commands.base import CommandFinished, CommandIds, ErrorIds
from .base import ClientCommandBase
from sft.common.utils.packets import (generate_header, get_payload_size, get_header_size)
from sft.common.config import Config


LOG = logging.getLogger(__name__)
_config = Config()
_packet_size = _config.package_size

__all__ = ['EchoCommand']


class EchoCommand(ClientCommandBase):
    """Usage: echo [text-to-transmit]"""
    @staticmethod
    def get_command_id():
        return CommandIds.ECHO_COMMAND_ID

    @staticmethod
    def get_command_alias():
        return 'echo'

    def _initialize(self, args_line):
        super()._initialize(args_line)

        data = bytearray(args_line, 'utf-8')
        ps = len(data)
        header = generate_header(self.get_command_id(), ErrorIds.SUCCESSFUL, ps)

        ending_zeros_amount = (_packet_size - (len(header) + ps) % _packet_size)
        data = header + data + (b'0' * ending_zeros_amount)
        self._data = [data[pos:pos + _packet_size] for pos in range(0, len(data), _packet_size)]

        self._write_finished = False
        self._reading_started = False
        self._packets_left_to_read = 0
        self._one_packet_command = False

    def receive_data(self, data):
        if not self._write_finished:
            return

        if not self._reading_started:
            self._reading_started = True
            ps = get_payload_size(data)
            command_size = get_header_size() + ps
            self._ending_zeros_amount = _packet_size - command_size % _packet_size
            self._packets_left_to_read = command_size // _packet_size + (1 if command_size % _packet_size > 0 else 0)
            if self._packets_left_to_read == 1:
                self._one_packet_command = True

        self._data.append(data)
        self._packets_left_to_read -= 1

        if self._packets_left_to_read == 0:
            self._data[0] = self._data[0][get_header_size():]
            ending_zeros_amount = self._ending_zeros_amount
            if self._one_packet_command:
                ending_zeros_amount += get_header_size()
            self._data[-1] = self._data[-1][:_packet_size - ending_zeros_amount]
            print('===>', b''.join(self._data).decode('utf-8'))
            raise CommandFinished

    def generate_data(self):
        if self._write_finished:
            return None

        data_len = len(self._data)
        if data_len > 0:
            data = self._data.pop(0)
            if data_len == 1:
                self._write_finished = True
            return data
