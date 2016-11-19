import logging
import abc

from sft.common.commands.base import ProgramFinished
from sft.common.config import Config


LOG = logging.getLogger(__name__)


class ServerBase(metaclass=abc.ABCMeta):
    """Basic server functionality."""
    def __init__(self):
        super().__init__()
        self._conf = Config()

    def run(self):
        self._initialize()
        try:
            LOG.debug('Server loop started')
            while True:
                self._main_loop()
        except ProgramFinished as e:
            pass
        except KeyboardInterrupt as e:
            pass
        finally:
            self._terminate()

    def _initialize(self):
        LOG.debug('Initializing server')

    @abc.abstractmethod
    def _main_loop(self):
        pass

    def _terminate(self):
        LOG.debug('Terminating server')
