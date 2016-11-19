import logging
import os

from sft.common.config import Config
from sft.common.commands.base import ServerCommandBase, CommandFinished, CommandIds, ErrorIds
from sft.common.utils.packets import get_payload, generate_packet, generate_header, get_error_code


STORAGE_PATH = os.path.expanduser(os.path.join("~", "sft-dir"))
if not os.path.exists(STORAGE_PATH):
    os.mkdir(STORAGE_PATH)


LOG = logging.getLogger(__name__)
_config = Config()

__all__ = ['Download']


class Download(ServerCommandBase):
    def __init__(self, first_packet):

        self._file_path = os.path.join(STORAGE_PATH, get_payload(first_packet))

        self._sended_bytes = 0
        self._generate_first_packet = True
        self._send_error = False
        self._wait_for_approve = False
        self._raise_command_finished = False

        if os.path.exists(self._file_path):
            self._file_size = os.path.getsize(self._file_path)
            self._file_descriptor = open(self._file_path, "rb")
        else:
            self._send_error = True

    @staticmethod
    def get_command_id():
        return CommandIds.DOWNLOAD_COMMAND_ID

    def _initialize(self, session_instance):
        pass

    def receive_data(self, data):

        if self._raise_command_finished:
            raise CommandFinished

        if get_error_code(data) == ErrorIds.DOWNLOAD_SUCCESSFUL:
            self._file_descriptor.close()

            print("Download finished")
            raise CommandFinished

    def generate_data(self):
        if self._wait_for_approve:
            return

        if self._raise_command_finished:
            raise CommandFinished

        if self._send_error:
            self._raise_command_finished = True
            return generate_packet(CommandIds.DOWNLOAD_COMMAND_ID, ErrorIds.ERROR, "File not found")

        # print("{}/{}".format(self._sended_bytes, self._file_size))

        if self._generate_first_packet:
            print("Generate download data")
            self._generate_first_packet = False
            header = generate_header(CommandIds.DOWNLOAD_COMMAND_ID, ErrorIds.SUCCESSFUL, self._file_size)

            if self._file_size + len(header) <= _config.package_size:
                package = header + self._file_descriptor.read()

                package = package + bytes(_config.package_size - len(package))
                self._wait_for_approve = True

                return package
            else:
                self._sended_bytes += _config.package_size - len(header)
                package = header + self._file_descriptor.read(_config.package_size - len(header))
                return package
        else:
            read_data = self._file_descriptor.read(_config.package_size)

            self._sended_bytes += len(read_data)
            if len(read_data) < _config.package_size:
                self._wait_for_approve = True
                return read_data + bytes(_config.package_size - len(read_data))
            else:
                return read_data
            # raise CommandFinished
