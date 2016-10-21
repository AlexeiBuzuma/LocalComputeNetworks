import logging
import abc


LOG = logging.getLogger(__name__)


class CommandFinished(Exception):
    pass


class CommandBase(metaclass=abc.ABCMeta):
    """Base class for all sft commands."""
    def __init__(self, first_packet_data):
        self._initialize(first_packet_data)

    @abc.abstractmethod
    def _initialize(self, first_packet_data):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_command_id():
        pass

    @abc.abstractmethod
    def recieve_data(self, data):
        pass

    @abc.abstractmethod
    def generate_data(self):
        pass
