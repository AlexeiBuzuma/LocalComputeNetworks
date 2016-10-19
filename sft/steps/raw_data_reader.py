""" This module contains functionality for DataReadingStep.
"""

from sft.config import Config

_config = Config()


def raw_data_tcp_reader(socket_list):
    """
    Receive data from tcp sockets.
    :param socket_list: List of sockets objects
    :return: [(client_addr, data), (client_addr, data), ...]
    """

    buffer_size = _config.tcp_buffer_size
    return [(socket.getpeername(), socket.recv(buffer_size)) for socket in socket_list]


def raw_data_udp_reader(socket_list):
    """
    Receive data from udp sockets.
    :param socket_list: List of sockets objects
    :return: [(client_addr, data), (client_addr, data), ...]
    """

    buffer_size = _config.udp_buffer_size
    return [socket.recvfrom(buffer_size) for socket in socket_list]
