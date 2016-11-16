import logging
import socket

from sft.server.base import ServerBase
from sft.drivers.loader import load_protocol_driver
from sft.common.steps import StepManager
from sft.common.commands.factory import CommandFactory
from sft.server.commands import load_commands
from sft.common.socket_manager import SocketManager


LOG = logging.getLogger(__name__)


class SFTServer(ServerBase):
    """SFT Server class.

       All server functionality is divided into 4 phases: socket selection,
       data reading, data writing and state check. All phases consist of
       execution steps which are influenced by active protocol driver.
       All steps of a phase are executed one by one, execution result of the
       previous step is given as an argument to the next step. Result of the
       last step becomes the result of the whole phase.
    """

    def __init__(self, protocol='tcp', host=None):
        super().__init__()
        self._protocol = protocol
        self._host = host

    def _initialize(self):
        load_protocol_driver(self._protocol)

        step_manager = StepManager("server")
        self._selection_steps = step_manager.get_selection_steps()
        self._reading_steps = step_manager.get_reading_steps()
        self._writing_steps = step_manager.get_writing_steps()
        self._state_check_steps = step_manager.get_state_check_steps()

        CommandFactory.init(load_commands())

        self._sock_manager = SocketManager()
        self._sock_manager.bind_server_socket(self._host)
        self._host = self._sock_manager.get_server_socket().getsockname()
        LOG.info('Starting server at %s:%d' % self._host)

    def _main_loop(self):
        self._sock_manager.update_selection()
        self._execute_steps(self._reading_steps)
        self._execute_steps(self._writing_steps)
        self._execute_steps(self._state_check_steps)

        from time import sleep; sleep(1)  # debug

    def _terminate(self):
        self._sock_manager.clear()

    @staticmethod
    def _execute_steps(steps, initial_arg=None):
        result = initial_arg
        for step in steps:
            result = step(result)
        return result
