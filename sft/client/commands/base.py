import logging
import abc
from sft.common.commands.base import CommandBase
from sft.client.cli import enable_cli_input, disable_cli_input


LOG = logging.getLogger(__name__)


class ClientCommandBase(CommandBase):
    """Base class for client-side commands.

       Docstring of your command class will be used as a help string for
       your command in client cli.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        disable_cli_input()

    @abc.abstractmethod
    def _initialize(self, line):
        """line argument is an argument string passed to command from cli."""
        pass

    @staticmethod
    @abc.abstractmethod
    def get_command_alias():
        """Return alias to call command from client cli.

           Return None if command mustn't be callable from cli.
        """
        pass

    def __del__(self):
        enable_cli_input()
