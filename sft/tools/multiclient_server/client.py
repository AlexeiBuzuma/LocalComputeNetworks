#!/usr/bin/env python
import socket
import sys
import logging
import argparse
import time


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(levelname)s:%(message)s')
LOG = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('server', help='sft-multiclient-server to connect')
    args = parser.parse_args()

    temp_server = args.server.split(':')
    temp_server[1] = int(temp_server[1])
    args.server = tuple(temp_server)

    return args


def connect_to_server(server):
    sock = socket.socket()
    sock.connect(server)
    LOG.info('Connected to %s:%d' % server)
    for _ in range(5):
        msg = b'ololo'
        LOG.info('Sending %r to server' % msg)
        sock.send(msg)
        time.sleep(1)
    sock.close()


def main():
    args = _parse_args()
    LOG.info('Client started')
    connect_to_server(args.server)
    LOG.info('Client terminated')


if __name__ == '__main__':
    main()
