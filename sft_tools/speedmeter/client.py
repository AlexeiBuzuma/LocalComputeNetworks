#!/usr/bin/env python3
import socket
import sys
import logging
import argparse


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(levelname)s:%(message)s')
LOG = logging.getLogger(__name__)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('server', help='sft-testspeed server to connect')
    parser.add_argument('filename', help='name of the file to transmit')
    args = parser.parse_args()

    temp_server = args.server.split(':')
    temp_server[1] = int(temp_server[1])
    args.server = tuple(temp_server)

    return args


def transmit_file(server_addr, file_name):
    s = socket.socket()
    try:
        s.connect(server_addr)
    except ConnectionRefusedError as e:
        LOG.error('Server is not started on %s:%d!' % server_addr)
        return

    with open(file_name, "rb") as f:
        l = f.read(1024)
        while (l):
            s.send(l)
            l = f.read(1024)

    s.close()
    LOG.info('Uploading completed')


def main():
    args = _parse_args()
    transmit_file(args.server, args.filename)


if __name__ == '__main__':
    main()
