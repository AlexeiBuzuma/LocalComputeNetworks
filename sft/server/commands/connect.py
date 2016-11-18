import logging

from sft.common.commands.base import ServerCommandBase, CommandFinished, CommandIds, ErrorIds
from sft.common.utils.packets import get_payload, generate_packet


LOG = logging.getLogger(__name__)

__all__ = ['Connect']


class Connect(ServerCommandBase):
    # ToDo: implement server's connect command logic
    def __init__(self, session_instance):
        self._initialize(session_instance)

        # ToDo: replace this bullshit with smt else?? (but is it real? I think no)
        self._send_response_flag = None
        self._raise_command_finished = None

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
        LOG.info("Created new session: {}".format(str(self.session_instance)))
        self._send_response_flag = True

    def generate_data(self):
        if self._raise_command_finished:
            raise CommandFinished

        if self._send_response_flag:
            self._raise_command_finished = True
            return generate_packet(CommandIds.CONNECT_COMMAND_ID.value, ErrorIds.CONNECTION_SUCCESSFUL.value, "")
        return None
