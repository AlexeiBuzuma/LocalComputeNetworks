import logging
import uuid

from sft.common.config import Config
from sft.common.commands.base import CommandBase, CommandFinished, CommandIds, ErrorIds
from sft.common.utils.packets import generate_packet, get_error_code, get_payload


LOG = logging.getLogger(__name__)
_config = Config()

__all__ = ['Connect']


class Connect(CommandBase):
    # ToDo: implement client's connect command logic
    def __init__(self, session_instance):
        self._initialize(session_instance)
        self._client_uuid = None
        self._generate_next = True

    @staticmethod
    def get_command_id():
        return CommandIds.CONNECT_COMMAND_ID

    def _initialize(self, session_instance):
        LOG.debug('Connect command instance created. '
                  'Session_instance: %r', session_instance)
        self.session_instance = session_instance

    def receive_data(self, data):
        LOG.info('Connected to %s:%d' % self.session_instance.client_address)

        if data and get_error_code(data) == ErrorIds.CONNECTION_SUCCESSFUL.value:
            self.session_instance.activate_session(self._client_uuid)
            LOG.info("Created new session: {}".format(str(self.session_instance)))
            raise CommandFinished

    def generate_data(self):

        # ToDo: uuid recovering

        if self._generate_next:
            self._generate_next = False
            self._client_uuid = str(uuid.uuid4())
            return generate_packet(CommandIds.CONNECT_COMMAND_ID.value, 0, self._client_uuid)
        else:
            return None
