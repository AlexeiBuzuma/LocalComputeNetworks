""" Dummy client
"""

import os
import socket
from time import sleep


UDP_MESSAGE_SIZE = 40000
UDP_TAIL = bytearray(b"UDP TAIL")


def run_tcp_client(ip, port, debug):

    s = socket.socket()
    s.connect((ip, port))
    number_of_message = 0

    while True:
        message = bytearray("This is beutiful message from client with number: {0}!\n"
                            .format(number_of_message), 'utf-8')
        if debug:
            print("Sending message: {0}... ".format(message))
        s.send(message)
        number_of_message += 1
        sleep(0.9)


def run_udp_client(ip, port, debug):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    number_of_message = 0

    while True:
        head_message = bytearray("Message number: {0}!".format(number_of_message), 'utf-8')

        junk_size = UDP_MESSAGE_SIZE - len(head_message) - len(UDP_TAIL)
        junk = os.urandom(junk_size)
        message = head_message + junk + UDP_TAIL

        if debug:
            print("Sending message: {0}... ".format(head_message))

        client_socket.sendto(message, (ip, port))

        number_of_message += 1
