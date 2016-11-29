import logging
import select
import socket

from sft.common.utils.common import Singleton


LOG = logging.getLogger(__name__)


class SocketManager(metaclass=Singleton):
    """Centralized point of socket control."""

    def __init__(self):
        self._sockets = {}
        self._readable = []
        self._writable = []
        self._exceptional = []
        self._server_socket = None

    def get_server_socket(self):
            return self._server_socket

    def get_socket_by_address(self, address):
        if address in self._sockets:
            return self._sockets[address]
        elif self._server_socket and self._server_socket.getpeername() == address:
            return self._server_socket
        else:
            raise ValueError("Socket with address '{}' does'nt exist".format(address))

    def add_socket(self, sock, address=None):
        if address is None:
            address = sock.getsockname()
        self._sockets[address] = sock

    def delete_socket_by_address(self, address):
        sock = self._sockets.pop(address)
        if sock is not None:
            for sock_list in (self._readable, self._writable, self._exceptional):
                if sock in sock_list:
                    sock_list.remove(sock)
            sock.close()

    def update_selection(self):
        sockets = self._sockets.values()
        self._readable, self._writable, self._exceptional =\
            select.select(sockets, sockets, sockets)
        # LOG.debug('R: %r' % self._readable)
        # LOG.debug('W: %r' % self._writable)
        # LOG.debug('E: %r' % self._exceptional)

    def get_readable_sockets(self):
        return self._readable

    def get_writable_sockets(self):
        return self._writable

    def get_exceptional_sockets(self):
        return self._exceptional

    def bind_server_socket(self, address=None):
        if address is None:
            address = (socket.gethostname(), 0)
        self._server_socket = self._bind_socket(*address)
        self._sockets['server_socket'] = self._server_socket
        self._server_socket.listen(10)

    def connect_to_server_socket(self, address):
        self._server_socket = self._connect_to_socket(address)
        self._sockets['server_socket'] = self._server_socket

    def clear(self):
        for sock in self._sockets.values():
            sock.close()
        self._sockets.clear()
        self._writable.clear()
        self._readable.clear()
        self._exceptional.clear()
        self._server_socket = None

    @staticmethod
    def _connect_to_socket(address):
        sock = socket.socket()
        sock.connect(address)
        return sock

    @staticmethod
    def _bind_socket(hostname=socket.gethostname(), port=0):
        sock = socket.socket()
        sock.bind((hostname, port))
        return sock
