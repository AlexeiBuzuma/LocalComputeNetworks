import logging

from sft.common.commands.base import CommandFinished, CommandIds
from .base import ClientCommandBase


LOG = logging.getLogger(__name__)

__all__ = ['SampleCommand']


class SampleCommand(ClientCommandBase):
    """Client command implementation example."""
    @staticmethod
    def get_command_id():
        return CommandIds.SAMPLE_COMMAND_ID

    @staticmethod
    def get_command_alias():
        return 'sample'

    def _initialize(self, args_line):
        super()._initialize(args_line)
        LOG.info('SampleCommand instance created. '
                 'Arguments line given: %r', args_line)

    def receive_data(self, data):
        raise CommandFinished

    def generate_data(self):
        return None
