import logging
from sft.common.config import Config


LOG = logging.getLogger(__name__)

_config = Config()


def raw_data_reader(data):
    """Receive data from tcp sockets.

       :param socket_list: List whith only one socket for reading data
       :return: [(server_addr, data), ]
    """

    LOG.debug('Client tcp raw_data_reader step')
    LOG.debug("socket_list: {}".format(data))

    service_socket, socket_list = data
    buffer_size = _config.tcp_buffer_size

    raw_data = []
    for socket in socket_list:
        reading_data = socket.recv(buffer_size)
        client_addr = socket.getpeername()

        # Socket closed by server
        # ToDo: Ask user for trying reactivation
        if not data:
            raise Exception("Server socket closed")

        raw_data = [(client_addr, data)]

    return raw_data
