#!/usr/bin/env python3
import logging

import argparse
import sys

import socket
import select

from port_for import select_random as get_random_port
from sft.utils.collections import SockCollection
from sft.common.config import Config


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(levelname)s:%(message)s')
LOG = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int)
    args = parser.parse_args()
    return args


class SFTServer():
    def __init__(self, port=None):
        super().__init__()
        self._conf = Config()
        self._sockets = SockCollection([], [])

        self._service_sock = self._create_socket_on_port(port=port)
        self._service_sock.listen(10)
        self._register_input_sock(self._service_sock)

        LOG.info('Server created on %s:%d' % self._service_sock.getsockname())

    def run(self):
        LOG.info('Server started')
        try:
            while True:
                self._main_loop()
        except KeyboardInterrupt as e:
            LOG.info('Terminating server')
            self._terminate()

    def _main_loop(self):
        self._check_sockets()

    def _terminate(self):
        for sock in self._sockets.inputs:
            self._unregister_sock(sock)
        for sock in self._sockets.outputs:
            self._unregister_sock(sock)

    def _register_input_sock(self, sock):
        self._sockets.inputs.append(sock)

    def _register_output_sock(self, sock):
        self._sockets.outputs.append(sock)

    def _unregister_sock(self, sock):
        if sock in self._sockets.inputs:
            self._sockets.inputs.remove(sock)
        if sock in self._sockets.outputs:
            self._sockets.outputs.remove(sock)
        sock.close()

    def _create_socket_on_port(self, port=None, hostname='localhost'):
        sock = socket.socket()
        if port is None:
            while True:
                try:
                    port = get_random_port()
                    sock.bind((hostname, port))
                except Exception as e:
                    pass
                else:
                    break
        else:
            sock.bind((hostname, port))
        return sock

    def _check_sockets(self):
        inputs = self._sockets.inputs
        outputs = self._sockets.outputs
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for sock in exceptional:
            self._unregister_sock(sock)
        for sock in readable:
            if sock == self._service_sock:
                client_sock, client_addr = sock.accept()
                LOG.info('Client %s:%d connected' % client_addr)
                self._register_input_sock(client_sock)
            else:
                client_addr = sock.getpeername()
                data = sock.recv(self._conf.tcp_buffer_size)
                if data:
                    LOG.info('%s:%d transmitted ' % client_addr + str(data))
                else:
                    LOG.info('Client %s:%d disconnected' % client_addr)
                    self._unregister_sock(sock)


def main():
    try:
        args = _parse_args()
        server = SFTServer(args.port)
        server.run()
    except KeyboardInterrupt as e:
        LOG.info('Exiting')


if __name__ == '__main__':
    main()
