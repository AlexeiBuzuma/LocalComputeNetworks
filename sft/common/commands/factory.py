import logging

from sft.common.commands import load_commands  # delete me!!!
from sft.common.utils.common import Singleton
from sft.common.utils.packets import get_command_id


LOG = logging.getLogger(__name__)


class CommandFactory(metaclass=Singleton):
    # ToDo: add __init__ argument for commands
    def __init__(self):
        super().__init__()
        self._commands_by_id = load_commands()

    def create_command(self, first_packet_data):
        # ToDo: If command is CONNECT return None
        com_id = get_command_id(first_packet_data)
        try:
            return self._commands_by_id[com_id](first_packet_data)
        except KeyError as e:
            raise ValueError('There is no command with given id (%d)' % com_id)

    # ToDo: implement get_command_by_id(self, command_id)
