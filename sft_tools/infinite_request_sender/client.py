""" Dummy client
"""

import os
import socket
from time import sleep


MESSAGE_SIZE = 1024
UDP_TAIL = bytearray(b"UDP TAIL")


def run_tcp_client(ip, port, debug):
    s = socket.socket()
    s.connect((ip, port))

    try:
        while True:
            message = b'\x63' * MESSAGE_SIZE
            if debug:
                print("Sending message: {0}... ".format(message))
            s.send(message)
            sleep(0.9)
    except KeyboardInterrupt:
        pass
    finally:
        s.close()


def run_udp_client(ip, port, debug):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    number_of_message = 0

    while True:
        head_message = bytearray("Message number: {0}!".format(number_of_message), 'utf-8')

        junk_size = MESSAGE_SIZE - len(head_message) - len(UDP_TAIL)
        junk = os.urandom(junk_size)
        message = head_message + junk + UDP_TAIL

        if debug:
            print("Sending message: {0}... ".format(head_message))

        client_socket.sendto(message, (ip, port))

        number_of_message += 1
