import logging
import uuid

from sft.common.commands.factory import CommandFactory
from sft.common.config import Config
from sft.common.commands.base import CommandFinished, CommandIds, ErrorIds, ProgramFinished
from .base import ClientCommandBase
from sft.common.utils.packets import generate_packet, get_error_code, get_command_id
from sft.common.sessions.session_manager import SessionManager
from sft.common.utils.storage import load_client_data, delete_client_data


LOG = logging.getLogger(__name__)
_config = Config()
_session_manager = SessionManager()

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
        self._need_reactivation = False
        self.session_instance = session_instance

    def receive_data(self, data):
        LOG.info('Server %s:%d: logical connection established' % self.session_instance.client_address)

        if data:
            if get_command_id(data) != CommandIds.CONNECT_COMMAND_ID:
                LOG.warning('Unexpected command packet arrived!')
                return

            error_code = get_error_code(data)

            if error_code == ErrorIds.SUCCESSFUL:
                if self._need_reactivation:
                    LOG.warning('Server denied session reactivation')
                    delete_client_data()
                _session_manager.activate_session(session=self.session_instance, uuid=self._client_uuid)
                raise CommandFinished
            elif error_code == ErrorIds.CONNECT_SESSION_REACTIVATION:
                if not self._need_reactivation:
                    LOG.error('Server reactivated session, but no session had been saved on client side')
                    raise ProgramFinished(ErrorIds.ERROR)
                download_command = CommandFactory().get_command_by_id(CommandIds.DOWNLOAD_COMMAND_ID)
                download_command = download_command(None)
                download_command.IS_COMMAND_RESTORED = True
                self.session_instance.command = download_command
                _session_manager.activate_session(session=self.session_instance, uuid=self._client_uuid)
                LOG.info('Session has been successfully reactivated')

    def generate_data(self):
        if self._generate_next:
            self._generate_next = False
            client_data = load_client_data()
            if client_data:
                LOG.info('Last session was ended inappropriately. Trying to restore session')
                self._client_uuid = client_data['uuid']
                self._need_reactivation = True
            else:
                self._client_uuid = str(uuid.uuid4())
            return generate_packet(CommandIds.CONNECT_COMMAND_ID, 0, self._client_uuid)
        else:
            return None
