import logging

from sft.client.base import ClientBase
from sft.common.commands.base import ProgramFinished
from sft.drivers.loader import load_protocol_driver
from sft.common.steps import StepManager
from sft.common.commands.factory import CommandFactory
from sft.client.commands import load_commands
from sft.common.socket_manager import SocketManager


LOG = logging.getLogger(__name__)


class SFTClient(ClientBase):
    """Write me!!!"""

    sockets = dict()

    def __init__(self, protocol='tcp', server_address=None):
        super().__init__()
        self._protocol = protocol
        self._server_address = server_address

    def _initialize(self):
        load_protocol_driver(self._protocol)

        step_manager = StepManager("client")
        self._selection_steps = step_manager.get_selection_steps()
        self._reading_steps = step_manager.get_reading_steps()
        self._writing_steps = step_manager.get_writing_steps()
        self._state_check_steps = step_manager.get_state_check_steps()

        CommandFactory.init(load_commands())

        self._sock_manager = SocketManager()
        self._sock_manager.connect_to_server_socket(self._server_address)
        self._host = self._sock_manager.get_server_socket().getsockname()
        LOG.info('Clent connected to %s:%d' % self._server_address)

    def _main_loop(self):
        self._sock_manager.update_selection()
        self._execute_steps(self._reading_steps)
        self._execute_steps(self._writing_steps)
        self._execute_steps(self._state_check_steps)

        # from time import sleep; sleep(1)  # debug

    def _terminate(self):
        self._sock_manager.clear()

    @staticmethod
    def _execute_steps(steps, initial_arg=None):
        result = initial_arg
        for step in steps:
            result = step(result)
        return result
