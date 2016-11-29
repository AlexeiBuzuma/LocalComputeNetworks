import logging

from sft.common.config import Config
from sft.common.utils.common import run_once


LOG = logging.getLogger(__name__)


def load_protocol_driver(protocol=None):
    get_protocol_driver(protocol)


@run_once
def get_protocol_driver(protocol=None):
    """Load appropriate protocol driver."""
    if protocol is None:
        try:
            protocol = Config().protocol
        except Exception as e:
            raise RuntimeError('Protocol not specified')
    if protocol == 'tcp':
        from sft.drivers.tcp import TCPDriver  # don't move to the top!
        return TCPDriver()
    elif protocol == 'udp':
        from sft.drivers.udp import UDPDriver  # don't move to the top!
        return UDPDriver()
    else:
        raise RuntimeError('Unknown protocol specified')
    # LOG.debug('%s driver loaded', protocol)
