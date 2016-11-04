import logging
import socket

from sft.common.config import Config
from sft.client.base import ClientBase
from sft.drivers.loader import load_protocol_driver
from sft.common.steps import StepManager
from port_for import select_random as get_random_port


LOG = logging.getLogger(__name__)


class SFTClient(ClientBase):
    """Write me!!!"""

    sockets = dict()

    def __init__(self, protocol='tcp', host=None):
        super().__init__()
        load_protocol_driver(protocol)
        step_manager = StepManager()
        self._selection_steps = step_manager.get_selection_steps()
        self._reading_steps = step_manager.get_reading_steps()
        self._writing_steps = step_manager.get_writing_steps()
        self._state_check_steps = step_manager.get_state_check_steps()

        # ToDo: get port from config ot command line args
        self.sockets['service_socket'] = self._create_socket_on_port(port=33333)
        self.sockets['service_socket'].listen(10)
        # ToDo: initialize command factory

    def _main_loop(self):
        selection_step_args = (self.sockets['service_socket'], list(self.sockets.values()))
        readable, writable, exceptional = self._execute_steps(self._selection_steps, selection_step_args)

        self._execute_steps(self._reading_steps, (self.sockets['service_socket'], readable))
        self._execute_steps(self._writing_steps, (self.sockets['service_socket'], writable))
        self._execute_steps(self._state_check_steps)

        from time import sleep; sleep(1)  # debug

    def _execute_steps(self, steps, initial_arg=None):
        result = initial_arg
        for step in steps:
            result = step(result)
        return result

    @staticmethod
    def _create_socket_on_port(port=None, hostname='localhost'):
        sock = socket.socket()
        if port is None:
            while True:
                try:
                    port = get_random_port()
                    sock.bind((hostname, port))
                except Exception as e:
                    pass
                else:
                    break
        else:
            sock.bind((hostname, port))
        return sock

sockets = SFTClient.sockets
