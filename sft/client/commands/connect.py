import logging

from sft.common.config import Config
from sft.common.commands.base import CommandBase, CommandFinished, CommandIds
from sft.common.utils.packets import generate_packet, get_error_code


LOG = logging.getLogger(__name__)
_config = Config()

__all__ = ['Connect']


class Connect(CommandBase):
    # ToDo: implement client's connect command logic
    def __init__(self, session_instance):
        self._initialize(session_instance)

    @staticmethod
    def get_command_id():
        return CommandIds.CONNECT_COMMAND_ID

    def _initialize(self, session_instance):
        LOG.debug('Connect command instance created. '
                  'Session_instance: %r', session_instance)
        self.session_instance = session_instance

    def receive_data(self, data):
        # self.session_instance.activate_session('session_ololo')
        print(self.session_instance)
        LOG.info('Connected to %s:%d' % self.session_instance.client_address)

        if data and get_error_code(data) == 1:
            raise CommandFinished
        # raise CommandFinished

    def generate_data(self):

        # ToDo: write function thar will be encapsulate package creation (utils.common)
        # ToDo: get sizes from config
        print("CLIENT SEND")

        uuid = "13666"
        return generate_packet(0, CommandIds.CONNECT_COMMAND_ID.value, 0, uuid)
        # return bytes(CommandIds.CONNECT_COMMAND_ID) + bytes(1023)
