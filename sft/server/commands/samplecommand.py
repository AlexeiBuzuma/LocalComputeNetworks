import logging

from sft.common.commands.base import ServerCommandBase, CommandFinished, CommandIds


LOG = logging.getLogger(__name__)

__all__ = ['SampleCommand']


class SampleCommand(ServerCommandBase):
    """Command implementation example."""
    @staticmethod
    def get_command_id():
        return CommandIds.SAMPLE_COMMAND_ID

    def _initialize(self, first_packet_data):
        # LOG.debug('SampleCommand instance created. '
        #           'First packet: %r', first_packet_data)
        pass

    def receive_data(self, data):
        raise CommandFinished

    def generate_data(self):
        return None
