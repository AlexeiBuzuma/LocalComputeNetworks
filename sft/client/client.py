import logging
import socket

from sft.client.base import ClientBase
from sft.drivers.loader import load_protocol_driver
from sft.common.steps import StepManager
from sft.common.commands.factory import CommandFactory
from sft.client.commands import load_commands


LOG = logging.getLogger(__name__)


class SFTClient(ClientBase):
    """Write me!!!"""

    sockets = dict()

    def __init__(self, protocol='tcp', host=None):
        super().__init__()
        self._protocol = protocol
        self._host = host

    def _initialize(self):
        load_protocol_driver(self._protocol)

        step_manager = StepManager("client")
        self._selection_steps = step_manager.get_selection_steps()
        self._reading_steps = step_manager.get_reading_steps()
        self._writing_steps = step_manager.get_writing_steps()
        self._state_check_steps = step_manager.get_state_check_steps()

        CommandFactory.init(load_commands())

        if self._host is None:
            self._host = ('localhost', None)
        self.sockets['service_socket'] = service_socket = self._create_socket(*self._host)
        service_socket.listen(10)
        LOG.info('Starting server at %s:%d' % service_socket.getsockname())

    def _main_loop(self):
        selection_step_args = (self.sockets['service_socket'], list(self.sockets.values()))
        readable, writable, exceptional = self._execute_steps(self._selection_steps, selection_step_args)

        self._execute_steps(self._reading_steps, (self.sockets['service_socket'], readable))
        self._execute_steps(self._writing_steps, (self.sockets['service_socket'], writable))
        self._execute_steps(self._state_check_steps)

        from time import sleep; sleep(1)  # debug

    def _terminate(self):
        for sock in self.sockets.values():
            sock.close()
        self.sockets.clear()

    @staticmethod
    def _execute_steps(steps, initial_arg=None):
        result = initial_arg
        for step in steps:
            result = step(result)
        return result

    @staticmethod
    def _create_socket(hostname='localhost', port=None):
        sock = socket.socket()
        if port is None:
            port = 0
        sock.bind((hostname, port))
        return sock

sockets = SFTClient.sockets
