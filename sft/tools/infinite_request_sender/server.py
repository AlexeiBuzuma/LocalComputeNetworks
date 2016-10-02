""" Dummy server
"""

import socket
from time import sleep


def _run_server(port, debug):

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

run = _run_server
