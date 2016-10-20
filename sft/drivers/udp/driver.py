import logging
from copy import deepcopy

from sft.drivers.base import ProtocolDriverBase
from sft.drivers.udp.server.steps import steps


LOG = logging.getLogger(__name__)


class UDPDriver(ProtocolDriverBase):
    """SFT UDP protocol driver."""
    def __init__(self):
        super().__init__()

    def get_server_steps(self):
        return deepcopy(steps)
