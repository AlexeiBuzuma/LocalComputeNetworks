import logging

from sft.common.commands.base import CommandFinished, ServerCommandBase, CommandIds, ErrorIds
from sft.common.socket_manager import SocketManager
from sft.common.utils.packets import (generate_packet, get_payload)
from sft.common.config import Config
from sft.common.sessions.session_manager import SessionManager


LOG = logging.getLogger(__name__)
_config = Config()
_packet_size = _config.package_size
_session_manager = SessionManager()

__all__ = ['CloseCommand']


class CloseCommand(ServerCommandBase):
    @staticmethod
    def get_command_id():
        return CommandIds.CLOSE_COMMAND_ID

    def _initialize(self, first_packet_data):
        LOG.debug('CloseCommand instance created.')

        self._uuid = get_payload(first_packet_data)
        self._client_address = SessionManager().delete_session_by_uuid(self._uuid)
        if self._client_address is not None:
            SocketManager().delete_socket_by_address( self._client_address)
        self._finished = True
        LOG.info('Client %s:%d: logical connection closed' % self._client_address)

    def receive_data(self, data):
        if self._finished:
            raise CommandFinished

    def generate_data(self):
        if self._finished:
            raise CommandFinished
