#!/usr/bin/env python3
import socket
import sys
import time
import logging
import argparse
from port_for import select_random as get_random_port
import tempfile


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


def bind_socket(sock_port):
    sock = socket.socket()
    sock_addr = 'localhost'
    if sock_port is None:
        while True:
            try:
                sock_port = get_random_port()
                sock.bind((sock_addr, sock_port))
            except Exception as e:
                pass
            else:
                break
    else:
        sock.bind((sock_addr, sock_port))
    LOG.info('Starting server on %s:%d' % (sock_addr, sock_port))
    return sock


def start_server(port):
    server_sock = bind_socket(port)
    server_sock.listen(10)
    conn_id = 0

    while True:
        client_sock, client_addr = server_sock.accept()
        LOG.info('Started downloading from %s:%d' % client_addr)
        byte_counter = 0
        conn_id += 1

        with tempfile.TemporaryFile() as f:
            start_time = time.time()
            l = client_sock.recv(1024)
            while (l):
                f.write(l)
                byte_counter += len(l)
                l = client_sock.recv(1024)
            end_time = time.time()

        f.close()
        client_sock.close()
        speed = byte_counter / (end_time - start_time) / 125000
        LOG.info('File downloaded, average speed %f Mbit' % speed)
    server_sock.close()


def main():
    try:
        args = _parse_args()
        start_server(args.port)
    except KeyboardInterrupt as e:
        LOG.info('Terminating server')


if __name__ == '__main__':
    main()
