import logging
import select
import socket

from sft.common.utils.common import Singleton


LOG = logging.getLogger(__name__)


class SocketManager(metaclass=Singleton):
    """Centralized point of socket control."""

    def __init__(self):
        self._sockets = {}
        self._sockets_list = []
        self.readable = []
        self.writable = []
        self.exceptional = []
        self.service_socket = None

    def get_socket_by_address(self, address):
        if address in self._sockets:
            return self._sockets[address]
        elif self.service_socket and self.service_socket.getpeername() == address:
            return self.service_socket
        else:
            raise ValueError("Socket with address '{}' does'nt exist".format(address))

    def add_socket(self, sock, address=None):
        if address is None:
            address = sock.getsockname()
        self._sockets[address] = sock
        self._sockets_list.append(sock)

    def delete_socket_by_address(self, address):
        sock = self._sockets.pop(address)
        if sock is not None:
            self._sockets_list.remove(sock)
            for sock_list in (self.readable, self.writable, self.exceptional):
                if sock in sock_list:
                    sock_list.remove(sock)
            sock.close()

    def update_selection(self):
        sockets = self._sockets_list
        self.readable, self.writable, self.exceptional =\
            select.select(sockets, sockets, sockets, 0.5)

    def bind_server_socket(self, address=None):
        if address is None:
            address = (socket.gethostname(), 0)
        self.service_socket = self._bind_socket(*address)
        self._sockets['service_socket'] = self.service_socket
        self._sockets_list.append(self.service_socket)
        self.service_socket.listen(10)

    def connect_to_server_socket(self, address):
        self.service_socket = self._connect_to_socket(address)
        self._sockets['service_socket'] = self.service_socket
        self._sockets_list.append(self.service_socket)

    def clear(self):
        for sock in self._sockets.values():
            sock.close()
        self._sockets.clear()
        self.writable.clear()
        self.readable.clear()
        self.exceptional.clear()
        self._sockets_list.clear()

    @staticmethod
    def _connect_to_socket(address):
        sock = socket.socket()
        sock.connect(address)
        return sock

    @staticmethod
    def _bind_socket(hostname=socket.gethostname(), port=0):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((hostname, port))
        return sock
