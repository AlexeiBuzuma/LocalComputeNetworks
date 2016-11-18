import logging
import uuid

from sft.common.config import Config
from sft.common.commands.base import CommandFinished, CommandIds, ErrorIds
from .base import ClientCommandBase
from sft.common.utils.packets import generate_packet, get_error_code, get_payload


LOG = logging.getLogger(__name__)
_config = Config()

__all__ = ['Connect']


class Connect(ClientCommandBase):
    @staticmethod
    def get_command_id():
        return CommandIds.CONNECT_COMMAND_ID

    @staticmethod
    def get_command_alias():
        return None

    def _initialize(self, session_instance):
        super()._initialize(None)
        self._client_uuid = None
        self._generate_next = True
        self.session_instance = session_instance
        LOG.debug('Connect command instance created. '
                  'Session_instance: %r', session_instance)

    def receive_data(self, data):
        LOG.info('Connected to %s:%d' % self.session_instance.client_address)

        if data and get_error_code(data) == ErrorIds.SUCCESSFUL:
            self.session_instance.activate_session(self._client_uuid)
            LOG.info("Created new session: {}".format(str(self.session_instance)))
            raise CommandFinished

    def generate_data(self):

        # ToDo: uuid recovering

        if self._generate_next:
            self._generate_next = False
            self._client_uuid = str(uuid.uuid4())
            return generate_packet(CommandIds.CONNECT_COMMAND_ID, 0, self._client_uuid)
        else:
            return None
