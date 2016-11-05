import logging
from copy import deepcopy

from sft.drivers.base import ProtocolDriverBase


LOG = logging.getLogger(__name__)


class TCPDriver(ProtocolDriverBase):
    """SFT TCP protocol driver."""
    def get_server_steps(self):
        from sft.drivers.tcp.server.steps import steps as _server_steps
        return deepcopy(_server_steps)

    def get_client_steps(self):
        from sft.drivers.tcp.client.steps import steps as _client_steps
        return deepcopy(_client_steps)
