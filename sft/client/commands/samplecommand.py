import logging

from sft.common.commands.base import CommandBase, CommandFinished, CommandIds


LOG = logging.getLogger(__name__)

__all__ = ['Connect']


class Connect(CommandBase):
    def __init__(self, session_instance):
        self._initialize(session_instance)

    @staticmethod
    def get_command_id():
        return CommandIds.CONNECT_COMMAND_ID

    def _initialize(self, session_instance):
        LOG.debug('SampleCommand instance created. '
                  'Session_instance: %r', session_instance)
        self.session_instance = session_instance
        # check if state file exists
        # if exists read uid else generate new

    def recieve_data(self, data):
        # if recieve 
        raise CommandFinished

    def generate_data(self):
        return None
