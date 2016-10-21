import logging

from sft.server.commands.base import CommandBase


LOG = logging.getLogger(__name__)

__all__ = ['SampleCommand']


class SampleCommand(CommandBase):
    """Command implementation example."""
    def __init(self, first_packet_data):
        super().__init__()

    @property
    def command_id(self):
        return 0

    def recieve_data(self, data):
        pass

    def generate_data(self):
        pass
