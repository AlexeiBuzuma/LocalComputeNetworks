import logging
import abc


LOG = logging.getLogger(__name__)


class CommandBase(metaclass=abc.ABCMeta):
    """Base class for all sft commands."""
    @abc.abstractmethod
    def __init(self, first_packet_data):
        pass

    @abc.abstractproperty
    def command_id(self):
        pass

    @abc.abstractmethod
    def recieve_data(self, data):
        pass

    @abc.abstractmethod
    def generate_data(self):
        pass
