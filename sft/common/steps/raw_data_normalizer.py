import logging

import abc


LOG = logging.getLogger(__name__)


class DataNormalizerBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def normalize(self, data):
        pass


class DataNormalizer(DataNormalizerBase):
    def normalize(self, data):
        # LOG.debug('std raw_data_normalizer step')
        pass


raw_data_normalizer = DataNormalizer().normalize
