import logging

from sft.server.commands.base import CommandBase, CommandFinished


LOG = logging.getLogger(__name__)

__all__ = ['SampleCommand']


class SampleCommand(CommandBase):
    """Command implementation example."""
    @staticmethod
    def get_command_id():
        return 96

    def _initialize(self, first_packet_data):
        LOG.debug('SampleCommand instance created. '
                  'First packet: %r', first_packet_data)

    def recieve_data(self, data):
        raise CommandFinished

    def generate_data(self):
        return None
