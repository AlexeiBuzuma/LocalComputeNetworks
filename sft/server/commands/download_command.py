import logging
import os

from sft.common.config import Config
from sft.common.commands.base import ServerCommandBase, CommandFinished, CommandIds, ErrorIds
from sft.common.utils.packets import get_payload, generate_packet, generate_header, get_error_code


LOG = logging.getLogger(__name__)
_config = Config()

__all__ = ['Download']


class Download(ServerCommandBase):
    def __init__(self, first_packet):
        self._file_path = get_payload(first_packet)
        # ToDo: file path check

        print("Create download")
        self._file_path = "/home/cartman/Downloads/qt-unified-linux-x64-2.0.3-1-online.run"
        self._file_size = os.path.getsize(self._file_path)
        self._file_decriptor = open(self._file_path, "rb")

        self._sended_bytes = 0
        self._generate_first_packet = True
        self._wait_for_approve = False

    @staticmethod
    def get_command_id():
        return CommandIds.DOWNLOAD_COMMAND_ID

    def _initialize(self, session_instance):
        self.session_instance = session_instance
        # self._generate_first_packet = True

    def receive_data(self, data):
        if get_error_code(data) == ErrorIds.DOWNLOAD_SUCCESSFUL:
            self._file_decriptor.close()
            print("Download finished")
            raise CommandFinished

    def generate_data(self):
        if self._wait_for_approve:
            return

        # print("{}/{}".format(self._sended_bytes, self._file_size))

        if self._generate_first_packet:
            print("Generate download data")
            self._generate_first_packet = False
            header = generate_header(CommandIds.DOWNLOAD_COMMAND_ID, ErrorIds.SUCCESSFUL, self._file_size)

            if self._file_size + len(header) <= _config.package_size:
                package = header + self._file_decriptor.read()
                package = package + bytes(_config.package_size - len(package))
                self._wait_for_approve = True

                return package
            else:
                self._sended_bytes += _config.package_size - len(header)
                package = header + self._file_decriptor.read(_config.package_size - len(header))
                return package
        else:
            read_data = self._file_decriptor.read(_config.package_size)
            self._sended_bytes += len(read_data)
            if len(read_data) < _config.package_size:
                self._wait_for_approve = True
                return read_data + bytes(_config.package_size - len(read_data))
            else:
                return read_data
            # raise CommandFinished
