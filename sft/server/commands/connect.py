import logging
import uuid

from sft.common.commands.base import ServerCommandBase, CommandFinished, CommandIds, ErrorIds
from sft.common.utils.packets import get_payload, generate_packet, get_command_id
from sft.common.sessions.session_manager import SessionManager

LOG = logging.getLogger(__name__)

__all__ = ['Connect']
_session_manager = SessionManager()


class Connect(ServerCommandBase):
    def __init__(self, session_instance):
        self._initialize(session_instance)
        self._send_response_flag = None
        self._session_reactivated = False
        self._raise_command_finished = False

    @staticmethod
    def get_command_id():
        return CommandIds.CONNECT_COMMAND_ID

    def _initialize(self, session_instance):
        self.session_instance = session_instance

    def receive_data(self, data):
        if data:
            if get_command_id(data) != CommandIds.CONNECT_COMMAND_ID:
                LOG.warning('Client %s:%d: Unexpected command packet arrived!' % self.session_instance.client_address)
                return

            self._send_response_flag = True
            client_uuid = get_payload(data)
            session = _session_manager.get_session(client_uuid, create_new=False)
            if session is not None:
                self._session_reactivated = True
                self._reactivated_session = session
                _session_manager.delete_session(client_uuid)
                return
            _session_manager.activate_session(session=self.session_instance, uuid=client_uuid)

    def generate_data(self):
        if self._raise_command_finished:
            raise CommandFinished

        if self._send_response_flag:
            self._send_response_flag = False
            if self._session_reactivated:
                self.session_instance.command = self._reactivated_session.command
                LOG.info('Client %s:%d: logical connection restored' % self.session_instance.client_address)
                return generate_packet(CommandIds.CONNECT_COMMAND_ID, ErrorIds.CONNECT_SESSION_REACTIVATION, "")
            self._raise_command_finished = True
            LOG.info('Client %s:%d: logical connection established' % self.session_instance.client_address)
            return generate_packet(CommandIds.CONNECT_COMMAND_ID, ErrorIds.SUCCESSFUL, "")
        return None
