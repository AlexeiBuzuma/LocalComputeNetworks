import logging
import argparse
import shlex
import time
import os

from .base import ClientCommandBase
from sft.common.config import Config
from sft.common.commands.base import CommandFinished, CommandInvalid, CommandIds, ErrorIds
from sft.common.utils.packets import (generate_packet, generate_header, get_payload,
get_payload_size, get_header_size, get_error_code)


LOG = logging.getLogger(__name__)
_config = Config()

__all__ = ['Download']


# Create default download directory
STORAGE_PATH = os.path.expanduser(os.path.join("~", "sft-download-dir"))
if not os.path.exists(STORAGE_PATH):
    os.mkdir(STORAGE_PATH)


def _parse_args(line):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="file", help="Path to file for download", required=True)
    parser.add_argument("-d", dest="dest_path", help="Path to save")

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
        self._start_time = time.time()
        try:
            args = _parse_args(first_packet_data)
        except SystemExit as e:
            raise CommandInvalid(str(e))

        self._create_default_download_dir()

        self._server_file_path = args.file
        self._client_file_path = os.path.join(STORAGE_PATH, args.file) if args.dest_path is None else args.dest_path
        self._client_file_descriptor = open(self._client_file_path, "wb")

        self._server_file_size = None
        self._readed_bytes = 0

        self._generate_request_package = True
        self._first_recived_package = True
        self._send_approve = False
        self._raise_finished = False
        # self._header = generate_header(CommandIds.DOWNLOAD_COMMAND_ID, 0, len(self._file_path))

    @staticmethod
    def _create_default_download_dir():
        if not os.path.exists(STORAGE_PATH):
            os.mkdir(STORAGE_PATH)

    def receive_data(self, data):

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

                self._send_approve = True
            else:
                self._client_file_descriptor.write(data)
                self._readed_bytes += len(data)


        # print("{}/{}".format(self._readed_bytes, self._file_size))

    def generate_data(self):
        if self._raise_finished:
            self._client_file_descriptor.close()
            print("Download finished")
            print('time spent: %4fs' % (time.time() - self._start_time))
            raise CommandFinished

        if self._send_approve:
            print("Generate package")
            self._raise_finished = True

            return generate_packet(CommandIds.DOWNLOAD_COMMAND_ID, ErrorIds.DOWNLOAD_SUCCESSFUL, "")

        if self._generate_request_package:
            print("Generate package")
            self._generate_request_package = False
            return generate_packet(CommandIds.DOWNLOAD_COMMAND_ID, 0, self._server_file_path)
        else:
            return None
