import logging

from sft.server.steps.default import steps as _default_steps
from sft.drivers.loader import get_protocol_driver


LOG = logging.getLogger(__name__)


class StepManager(object):
    def __init__(self):
        super().__init__()
        self._steps = _default_steps
        driver_steps = get_protocol_driver().get_server_steps()
        self._steps.update(driver_steps)

        LOG.debug('Selection steps: %r', self.get_selection_steps())
        LOG.debug('Reading steps: %r', self.get_reading_steps())
        LOG.debug('Writing steps: %r', self.get_writing_steps())
        LOG.debug('State_check steps: %r', self.get_state_check_steps())

    def get_selection_steps(self):
        return self._steps['socket_selector']

    def get_reading_steps(self):
        return self._steps['raw_data_reader'] +\
            self._steps['lastrecv_timestamp_updater'] +\
            self._steps['raw_data_normalizer'] +\
            self._steps['heartbit_reciever'] +\
            self._steps['packet_dispatcher']

    def get_writing_steps(self):
        return self._steps['packet_payload_collector'] +\
            self._steps['heartbit_sender'] +\
            self._steps['lastsent_timestamp_updater'] +\
            self._steps['packet_data_writer']

    def get_state_check_steps(self):
        return self._steps['server_state_check']
