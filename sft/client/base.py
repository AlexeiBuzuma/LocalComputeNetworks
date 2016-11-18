import logging
import abc

from sft.common.config import Config

from prompt_toolkit.shortcuts import prompt, create_eventloop
from prompt_toolkit import AbortAction

from .cli.commands import Dispatcher
from .cli import is_cli_input_disabled


LOG = logging.getLogger(__name__)


class ClientBase(metaclass=abc.ABCMeta):
    """Basic client functionality."""
    prompt = 'SFT: '

    def __init__(self):
        super().__init__()
        self._conf = Config()
        self.cmd_dispatcher = Dispatcher()

    def run(self):
        self._initialize()
        try:
            LOG.debug('Client loop started')
            while True:
                self._prompt_loop()
        except KeyboardInterrupt as e:
            pass
        finally:
            self._terminate()

    def _functional_loop(self, context):
        while is_cli_input_disabled() or not context.input_is_ready():
            self._main_loop()

    def _prompt_loop(self):
        text = prompt(
            self.prompt, patch_stdout=True, on_abort=AbortAction.RAISE_EXCEPTION,
            eventloop=create_eventloop(inputhook=self._functional_loop))
        self.cmd_dispatcher.onecmd(text)
        print()

        while is_cli_input_disabled():
            self._main_loop()

    def _initialize(self):
        LOG.debug('Initializing client')

    @abc.abstractmethod
    def _main_loop(self):
        pass

    def _terminate(self):
        LOG.debug('Terminating client')
