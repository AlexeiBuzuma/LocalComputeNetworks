#!/usr/bin/env python
import socket
import time


def main():
    sock = socket.socket()
    sock.connect(('localhost', 9899))
    for _ in range(5):
        sock.send(b'ololo')
        time.sleep(1)
    sock.close()


if __name__ == '__main__':
    main()
