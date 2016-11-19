import logging
import argparse
import shlex

from .base import ClientCommandBase
from sft.common.config import Config
from sft.common.commands.base import CommandFinished, CommandInvalid, CommandIds, ErrorIds
from sft.common.utils.packets import (generate_packet, generate_header, get_payload,
get_payload_size, get_header_size, get_error_code)


LOG = logging.getLogger(__name__)
_config = Config()

__all__ = ['Download']


def _parse_args(line):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="file", help="Path to file for download", required=True)

    return parser.parse_args(shlex.split(line))


class Download(ClientCommandBase):
    """Download command help"""
    @staticmethod
    def get_command_alias():
        return "download"

    @staticmethod
    def get_command_id():
        return CommandIds.DOWNLOAD_COMMAND_ID

    def _initialize(self, first_packet_data):
        try:
            print(first_packet_data)
            args = _parse_args(first_packet_data)
        except SystemExit as e:
            raise CommandInvalid(str(e))

        self._server_file_path = args.file
        self._client_file_path = "/home/cartman/file_to_save"
        self._client_file_descriptor = open(self._client_file_path, "wb")

        self._server_file_size = None
        self._readed_bytes = 0

        self._generate_request_package = True
        self._first_recived_package = True
        self._send_approve = False
        self._raise_finished = False
        # self._header = generate_header(CommandIds.DOWNLOAD_COMMAND_ID, 0, len(self._file_path))

    def receive_data(self, data):

        # print(data)
        if self._first_recived_package:
            if get_error_code(data) == ErrorIds.ERROR:
                print(get_payload(data))
                raise CommandFinished

            self._first_recived_package = False
            self._file_size = get_payload_size(data)

            if self._file_size + get_header_size() <= _config.package_size:
                self._client_file_descriptor.write(data[get_header_size():self._file_size+get_header_size()])
                self._send_approve = True
            else:
                self._client_file_descriptor.write(data[get_header_size():])
                self._readed_bytes += _config.package_size - get_header_size()
        else:
            if self._file_size - self._readed_bytes <= _config.package_size:
                self._client_file_descriptor.write(data[:self._file_size - self._readed_bytes])
                # print("bla")
                self._send_approve = True
            else:
                self._client_file_descriptor.write(data)
                self._readed_bytes += len(data)


        # print("{}/{}".format(self._readed_bytes, self._file_size))

    def generate_data(self):
        if self._raise_finished:
            self._client_file_descriptor.close()
            print("Download finished")
            raise CommandFinished

        if self._send_approve:
            print("Generate package")
            self._raise_finished = True
            return generate_packet(CommandIds.DOWNLOAD_COMMAND_ID, ErrorIds.DOWNLOAD_SUCCESSFUL, "Hi!")

        if self._generate_request_package:
            print("Generate package")
            self._generate_request_package = False
            return generate_packet(CommandIds.DOWNLOAD_COMMAND_ID, 0, self._server_file_path)
        else:
            return None
