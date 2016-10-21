import logging

from sft.config import Config
from sft.server.base import ServerBase
from sft.drivers.loader import load_protocol_driver
from sft.server.steps.manager import StepManager


LOG = logging.getLogger(__name__)


class SFTServer(ServerBase):
    """SFT Server class.

       All server functionality is devided into 4 phases: socket selection,
       data reading, data writing and state check. All phases consist of
       execution steps which are influenced by active protocol driver.
       All steps of a phase are executed one by one, execution result of the
       previous step is given as an argument to the next step. Result of the
       last step becomes the result of the whole phase.
    """

    sockets = dict()

    def __init__(self, protocol='tcp', host=None):
        super().__init__()
        load_protocol_driver(protocol)
        step_manager = StepManager()
        self._selection_steps = step_manager.get_selection_steps()
        self._reading_steps = step_manager.get_reading_steps()
        self._writing_steps = step_manager.get_writing_steps()
        self._state_check_steps = step_manager.get_state_check_steps()

    def _main_loop(self):
        self._execute_steps(self._selection_steps)
        self._execute_steps(self._reading_steps)
        self._execute_steps(self._writing_steps)
        self._execute_steps(self._state_check_steps)

        from time import sleep; sleep(1)  # debug

    def _execute_steps(self, steps, initial_arg=None):
        result = initial_arg
        for step in steps:
            result = step(result)
        return result

sockets = SFTServer.sockets
