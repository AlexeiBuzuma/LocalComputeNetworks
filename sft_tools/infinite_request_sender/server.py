""" Dummy server
"""

import os
import socket
from time import sleep


UDP_MESSAGE_SIZE = 4096


def run_tcp_server(port, debug):

    server_sock = socket.socket()
    server_addr = ("", port)
    server_sock.bind(server_addr)
    server_sock.listen(10)

    if debug:
        print('Starting server on port: %d' % server_addr[1])

    while True:
        client_sock, client_addr = server_sock.accept()
        print('Connecting with %s:%d' % client_addr)

        content = client_sock.recv(1024)
        while True:
            if not content:
                if debug:
                    print("Content is not received...")

                sleep(1)
                continue

            print(content)
            content = client_sock.recv(1024)
            sleep(0.3)


def run_udp_server(port, debug):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = ("", port)
    server_sock.bind(server_addr)

    if debug:
        print('Starting server on port: %d' % server_addr[1])

    while True:
        data, addr = server_sock.recvfrom(40000)
        print(data[:20], " ... ", data[-10:])
        sleep(0.01)
