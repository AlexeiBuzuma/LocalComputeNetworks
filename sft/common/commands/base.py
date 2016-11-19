import logging
import abc
from enum import IntEnum


LOG = logging.getLogger(__name__)


class CommandIds(IntEnum):
    CONNECT_COMMAND_ID = 1
    CLOSE_COMMAND_ID = 2
    HEARTBEAT_COMMAND_ID = 3
    TIME_COMMAND_ID = 4
    ECHO_COMMAND_ID = 5
    DOWNLOAD_COMMAND_ID = 6
    UPLOAD_COMMAND_ID = 7
    SAMPLE_COMMAND_ID = 99


class ErrorIds(IntEnum):
    SUCCESSFUL = 1
    ERROR = 2


class CommandFinished(Exception):
    pass


class ProgramFinished(Exception):
    def __init__(self, state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state


class CommandBase(metaclass=abc.ABCMeta):
    """Base class for all sft commands."""
    def __init__(self, *args, **kwargs):
        self._initialize(*args, **kwargs)

    @abc.abstractmethod
    def _initialize(self, *args, **kwargs):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_command_id():
        pass

    @abc.abstractmethod
    def receive_data(self, data):
        pass

    @abc.abstractmethod
    def generate_data(self):
        pass


class ServerCommandBase(CommandBase):
    @abc.abstractmethod
    def _initialize(self, first_packet_data):
        pass

