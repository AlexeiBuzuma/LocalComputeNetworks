import logging
import abc

from sft.common.config import Config


LOG = logging.getLogger(__name__)


class ClientBase(metaclass=abc.ABCMeta):
    """Basic server functionality."""
    def __init__(self):
        super().__init__()
        self._conf = Config()

    def run(self):
        self._initialize()
        try:
            LOG.info('Server started')
            while True:
                self._main_loop()
        except KeyboardInterrupt as e:
            pass
        finally:
            self._terminate()

    def _initialize(self):
        LOG.info('Initializing server')

    @abc.abstractmethod
    def _main_loop(self):
        pass

    def _terminate(self):
        LOG.info('Terminating server')
