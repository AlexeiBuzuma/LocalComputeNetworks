""" Dummy client
"""

import socket
from time import sleep


def _run_client(ip, port, debug):

    s = socket.socket()
    s.connect((ip, port))
    number_of_message = 0

    while True:
        message = bytearray("This is beutiful message from client with number: {0}!".format(number_of_message), 'utf-8')
        if debug:
            print("Sending message: {0}... ".format(message))
        s.send(message)
        number_of_message += 1
        sleep(0.9)

run = _run_client
