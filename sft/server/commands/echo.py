import logging

from sft.common.commands.base import CommandFinished, ServerCommandBase, CommandIds
from sft.common.utils.packets import (get_payload_size, get_header_size)
from sft.common.config import Config


LOG = logging.getLogger(__name__)
_config = Config()
_packet_size = _config.package_size

__all__ = ['EchoCommand']


class EchoCommand(ServerCommandBase):
    @staticmethod
    def get_command_id():
        return CommandIds.ECHO_COMMAND_ID

    def _initialize(self, first_packet_data):
        LOG.debug('EchoCommand instance created.')

        self._read_finished = False
        self._write_finished = False
        self._data = []
        self._packets_left_to_read = 0

        self._data.append(first_packet_data)
        LOG.debug('EchoCommand: reading %r' % first_packet_data)
        ps = get_payload_size(first_packet_data)
        command_size = get_header_size() + ps
        self._packets_left_to_read = command_size // _packet_size + (1 if command_size % _packet_size > 0 else 0)
        self._packets_left_to_read -= 1

        if self._packets_left_to_read == 0:
            self._read_finished = True
            LOG.debug('EchoCommand: reading finished')

    def receive_data(self, data):
        if self._write_finished:
            LOG.debug('EchoCommand: sending finished')
            raise CommandFinished
        if self._read_finished:
            return

        self._data.append(data)
        LOG.debug('EchoCommand: reading %r' % data)
        self._packets_left_to_read -= 1

        if self._packets_left_to_read == 0:
            self._read_finished = True
            LOG.debug('EchoCommand: reading finished')

    def generate_data(self):
        if self._write_finished:
            LOG.debug('EchoCommand: sending finished')
            raise CommandFinished
        if not self._read_finished:
            return None

        data_len = len(self._data)
        if data_len > 0:
            data = self._data.pop(0)
            LOG.debug('EchoCommand: sending %r' % data)
            if data_len == 1:
                self._write_finished = True
            return data
