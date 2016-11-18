import logging

from sft.common.utils.common import Singleton
from sft.common.utils.packets import get_command_id
from sft.common.commands.base import CommandIds


LOG = logging.getLogger(__name__)


class CommandFactory(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        LOG.debug('Command factory created. Loaded commands: %r' % self._commands_by_id)

    @classmethod
    def init(cls, commands):
        cls._commands_by_id = commands
        cls()

    def get_command_by_id(self, command_id):
        try:
            return self._commands_by_id[command_id]
        except KeyError as e:
            raise ValueError('There is no command with given id (%d)' % command_id)

    def create_command(self, first_packet_data):
        com_id = get_command_id(first_packet_data)
        if com_id == CommandIds.CONNECT_COMMAND_ID:
            return None
        return self.get_command_by_id(com_id)(first_packet_data)
