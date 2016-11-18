import logging
import time

from sft.common.commands.base import ServerCommandBase, CommandFinished, CommandIds, ErrorIds
from sft.common.utils.packets import get_payload, generate_packet


LOG = logging.getLogger(__name__)

__all__ = ['Time']


class Time(ServerCommandBase):
    def __init__(self, first_packet):
        self._raise_command_finished = None

    @staticmethod
    def get_command_id():
        return CommandIds.TIME_COMMAND_ID

    def _initialize(self, session_instance):
        self.session_instance = session_instance

    def receive_data(self, data):
        pass

    def generate_data(self):
        if self._raise_command_finished:
            raise CommandFinished

        self._raise_command_finished = True
        return generate_packet(CommandIds.TIME_COMMAND_ID, ErrorIds.SUCCESSFUL, str(time.ctime()))
