import logging
import abc


LOG = logging.getLogger(__name__)


class ProtocolDriverBase(object, metaclass=abc.ABCMeta):
    """Base class for sft protocol drivers."""
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def get_server_steps(self):
        pass
