#!/usr/bin/env python
import socket


def main():
    sock = socket.socket()
    sock.connect(('localhost', 9899))
    # sock.send(b'ololo')
    sock.close()


if __name__ == '__main__':
    main()
