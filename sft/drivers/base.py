import logging
import abc


LOG = logging.getLogger(__name__)


class ProtocolDriverBase(metaclass=abc.ABCMeta):
    """Base class for sft protocol drivers."""
    @abc.abstractmethod
    def get_server_steps(self):
        pass
