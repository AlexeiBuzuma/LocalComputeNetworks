import logging

from sft.config import Config
from sft.server.base import ServerBase
from sft.drivers.loader import DriverLoader
from sft.server.steps.manager import StepManager


LOG = logging.getLogger(__name__)


class SFTServer(ServerBase):
    def __init__(self, protocol='TCP', host=None):
        super().__init__()
        DriverLoader.load(protocol)
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

        from time import sleep; sleep(0.5)  # debug

    def _execute_steps(self, steps, initial_arg=None):
        result = initial_arg
        for step in steps:
            result = step(result)
        return result
