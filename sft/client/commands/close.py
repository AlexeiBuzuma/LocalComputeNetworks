import logging

from sft.common.commands.base import CommandFinished, ProgramFinished, CommandIds, ErrorIds
from sft.common.socket_manager import SocketManager
from .base import ClientCommandBase
from sft.common.utils.packets import (generate_packet, get_error_code)
from sft.common.config import Config
from sft.common.sessions.session_manager import SessionManager, SessionStatus

_socket_manager = SocketManager()


LOG = logging.getLogger(__name__)
_config = Config()
_packet_size = _config.package_size

__all__ = ['CloseCommand']


class CloseCommand(ClientCommandBase):
    """Usage: close"""
    @staticmethod
    def get_command_id():
        return CommandIds.CLOSE_COMMAND_ID

    @staticmethod
    def get_command_alias():
        return 'close'

    def _initialize(self, args_line):
        super()._initialize(args_line)
        LOG.debug('CloseCommand instance created.')

        self._send_request = True
        self._finish = False
        session = SessionManager().get_all_not_inactive_sessions()[0]
        client_uuid = session.client_uuid
        self._request = generate_packet(self.get_command_id(), ErrorIds.SUCCESSFUL, client_uuid)
        session.status = SessionStatus.wait_for_close

    def receive_data(self, data):
        pass

    def generate_data(self):
        if self._send_request:
            self._finish = True
            self._send_request = False
            return self._request
        return None

