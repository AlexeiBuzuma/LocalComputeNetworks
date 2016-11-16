import logging

from sft.common.commands.base import CommandBase, CommandFinished, CommandIds
from sft.common.utils.packets import get_payload, generate_packet


LOG = logging.getLogger(__name__)

__all__ = ['Connect']


class Connect(CommandBase):
    # ToDo: implement server's connect command logic
    def __init__(self, session_instance):
        self._initialize(session_instance)

        # ToDo: replace this bullshit with smt else
        self._flag = None

    @staticmethod
    def get_command_id():
        return CommandIds.CONNECT_COMMAND_ID

    def _initialize(self, session_instance):
        LOG.debug('Connect command instance created. '
                  'Session_instance: %r', session_instance)
        self.session_instance = session_instance

    def receive_data(self, data):
        # ToDo: session recovering

        uuid = get_payload(data)
        self.session_instance.activate_session(uuid)
        LOG.info('Client %s:%d: logical connection established' % self.session_instance.client_address)
        self._flag = 1
        # raise CommandFinished

    def generate_data(self):
        print("Generate data")
        if self._flag == 1:
            # ToDo: enumeration for all error codes status
            self._flag = None
            return generate_packet(0, CommandIds.CONNECT_COMMAND_ID.value, 1, "123")
        return None
