import logging

from sft.config import Config
from sft.utils.common import run_once
from sft.drivers.tcp import TCPDriver
from sft.drivers.udp import UDPDriver


LOG = logging.getLogger(__name__)


def load_protocol_driver(protocol=None):
    get_protocol_driver(protocol)


@run_once
def get_protocol_driver(protocol=None):
    if protocol is None:
        try:
            protocol = Config().protocol
        except Exception as e:
            raise RuntimeError('Protocol not specified')
    if protocol == 'TCP':
        return TCPDriver()
    elif protocol == 'UDP':
        return UDPDriver()
    else:
        raise RuntimeError('Unknown protocol specified')
    LOG.debug('%s driver loaded', protocol)
