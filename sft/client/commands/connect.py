import logging

from sft.common.commands.base import CommandBase, CommandFinished, CommandIds


LOG = logging.getLogger(__name__)

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
        self.session_instance.activate_session('session_ololo')
        LOG.info('Connected to %s:%d' % self.session_instance.client_address)
        raise CommandFinished

    def generate_data(self):
        return None
