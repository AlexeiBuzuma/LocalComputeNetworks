import logging

from .base import ClientCommandBase
from sft.common.config import Config
from sft.common.commands.base import CommandFinished, CommandIds, ErrorIds
from sft.common.utils.packets import generate_packet, get_error_code, get_payload


LOG = logging.getLogger(__name__)
_config = Config()

__all__ = ['Time']


class Time(ClientCommandBase):
    @staticmethod
    def get_command_alias():
        return "time"

    @staticmethod
    def get_command_id():
        return CommandIds.TIME_COMMAND_ID

    def _initialize(self, first_packet_data):
        self._generate_next = True

    def receive_data(self, data):
        print(get_payload(data))
        raise CommandFinished

    def generate_data(self):
        if self._generate_next:
            self._generate_next = False
            return generate_packet(CommandIds.TIME_COMMAND_ID, 0, "")
        else:
            return None
