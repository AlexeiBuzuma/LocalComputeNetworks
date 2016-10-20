import logging

from sft.config import Config
from sft.drivers.tcp import TCPDriver
from sft.drivers.udp import UDPDriver


LOG = logging.getLogger(__name__)


class DriverLoader():
    _driver = None

    @classmethod
    def load(cls, protocol=None):
        if protocol is None:
            try:
                protocol = Config().protocol
            except Exception as e:
                raise RuntimeError('Protocol not specified')
        if protocol == 'TCP':
            cls._driver = TCPDriver()
        elif protocol == 'UDP':
            cls._driver = UDPDriver()
        else:
            raise RuntimeError('Unknown protocol specified')
        LOG.debug('%s driver loaded', protocol)

    @classmethod
    def get_protocol_driver(cls):
        if cls._driver is None:
            cls.load()
        return cls._driver
