""" This module contains spaghetti implementation of Download command for client.
"""

import logging
import argparse
import shlex
import time
import os

from .base import ClientCommandBase
from sft.common.config import Config
from sft.common.utils.storage import save_client_data, delete_client_data, load_client_data
from sft.common.sessions.session_manager import SessionManager
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


class FileWriter:
    BUFFER_ITEMS_SIZE = 50

    def __init__(self, path):
        self._path = path
        self.start_file_size = os.path.getsize(self._path) if os.path.exists(self._path) else 0

        self._file_descriptor = open(self._path, "wb")

        self._current_index = 0
        self._buffer = bytearray()

    def write(self, data):
        self._current_index += 1
        self._buffer += data

        if self._current_index == self.BUFFER_ITEMS_SIZE:
            self.stash()

    def stash(self):
        if self._current_index != 0:
            self._file_descriptor.write(self._buffer)
            self._buffer = bytearray()
            self._current_index = 0

    def seek(self, offset):
        self._file_descriptor.seek(offset)

    def close(self):
        self.stash()
        self._file_descriptor.close()


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
        self._create_default_download_dir()

        self._current_sesion = SessionManager().get_all_not_inactive_sessions()[0]

        if first_packet_data is not None:
            try:
                args = _parse_args(first_packet_data)
            except SystemExit as e:
                raise CommandInvalid(str(e))

            self._server_file_path = args.file
            self._client_file_path = os.path.join(STORAGE_PATH, args.file) if args.dest_path is None else args.dest_path
            self._file_writer = FileWriter(self._client_file_path)
        else:
            self._server_file_path = None
            self._client_file_path = None
            self._file_writer = None

        self.IS_COMMAND_RESTORED = None
        self._command_restored_request_sended = None

        self._server_file_size = None
        self._readed_bytes = 0

        self._generate_request_package = True
        self._first_recived_package = True
        self._send_approve = False
        self._raise_finished = False

    def _write_client_data(self):
        client_data = dict(
            uuid=self._current_sesion.client_uuid,
            server_file_path=self._server_file_path,
            client_file_path=self._client_file_path,
            file_size=self._file_size,
        )

        save_client_data(client_data)

    def _load_client_data(self):
        client_data = load_client_data()

        if client_data is None:
            raise Exception("Can't read client data")

        self._server_file_path = client_data["server_file_path"]
        self._client_file_path = client_data["client_file_path"]
        self._file_size = client_data["file_size"]

        self._file_writer = FileWriter(self._client_file_path)

    @staticmethod
    def _create_default_download_dir():
        if not os.path.exists(STORAGE_PATH):
            os.mkdir(STORAGE_PATH)

    def receive_data(self, data):

        if self.IS_COMMAND_RESTORED:
            error_code = get_error_code(data)
            if error_code != ErrorIds.DOWNLOAD_POINTER_MOVED:
                return
            else:
                self.IS_COMMAND_RESTORED = False
                return

        if self._first_recived_package:
            if get_error_code(data) == ErrorIds.ERROR:
                print(get_payload(data))
                raise CommandFinished

            self._first_recived_package = False
            self._file_size = get_payload_size(data)

            self._write_client_data()

            if self._file_size + get_header_size() <= _config.package_size:
                self._file_writer.write(data[get_header_size():self._file_size+get_header_size()])
                self._send_approve = True
            else:
                self._file_writer.write(data[get_header_size():])
                self._readed_bytes += _config.package_size - get_header_size()
        else:
            if self._file_size - self._readed_bytes <= _config.package_size:
                self._file_writer.write(data[:self._file_size - self._readed_bytes])

                self._send_approve = True
            else:
                self._file_writer.write(data)
                self._readed_bytes += len(data)

    def generate_data(self):
        if self.IS_COMMAND_RESTORED and not self._command_restored_request_sended:
            self._command_restored_request_sended = True
            self._load_client_data()

            if self._file_writer.start_file_size <= _config.package_size:
                start_from = 0
            else:
                start_from = self._file_writer.start_file_size - _config.package_size

            self._file_writer.seek(start_from)

            return generate_packet(CommandIds.DOWNLOAD_COMMAND_ID, ErrorIds.DOWNLOAD_START_FROM, str(start_from))

        if self._raise_finished:
            self._file_writer.close()
            delete_client_data()

            print("Download finished")
            print('time spent: %4fs' % (time.time() - self._start_time))
            raise CommandFinished

        if self._send_approve:
            self._raise_finished = True

            return generate_packet(CommandIds.DOWNLOAD_COMMAND_ID, ErrorIds.DOWNLOAD_SUCCESSFUL, "")

        if self._generate_request_package:
            self._generate_request_package = False
            return generate_packet(CommandIds.DOWNLOAD_COMMAND_ID, 0, self._server_file_path)
        else:
            return None
