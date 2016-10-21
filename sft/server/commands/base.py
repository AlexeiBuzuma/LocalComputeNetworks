import logging
import abc

# ToDo: Is it a good place for this constants?
CONNECT_COMMAND_ID = 1
CLOSE_COMMAND_ID = 2
HEARTBIT_COMMAND_ID = 3
TIME_COMMAND_ID = 4
ECHO_COMMAND_ID = 5
DOWNLOAD_COMMAND_ID = 6
UPLOAD_COMMAND_ID = 7

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
