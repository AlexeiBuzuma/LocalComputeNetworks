import logging

from sft.common.steps import steps as _default_steps
from sft.drivers.loader import get_protocol_driver

LOG = logging.getLogger(__name__)


class StepManager:
    """Provides execution steps for each of server execution phases.

       Steps can differ based on driver loaded.
    """

    def __init__(self, role):
        """
        :param role: possible values: ["client", "server"]
        """

        self._role = role
        self._steps = dict()

        self._load_default_steps()
        self._load_role_steps()
        self._load_driver_steps()

        LOG.debug('Selection steps: %r', self.get_selection_steps())
        LOG.debug('Reading steps: %r', self.get_reading_steps())
        LOG.debug('Writing steps: %r', self.get_writing_steps())
        LOG.debug('State_check steps: %r', self.get_state_check_steps())

    def _load_default_steps(self):
        self._steps.update(_default_steps)

    def _load_role_steps(self):
        if self._role == "server":
            from sft.server.steps import steps as _server_steps
            self._steps.update(_server_steps)
        elif self._role == "client":
            from sft.client.steps import steps as _client_steps
            self._steps.update(_client_steps)

    def _load_driver_steps(self):
        if self._role == "server":
            self._steps.update(get_protocol_driver().get_server_steps())
        elif self._role == "client":
            self._steps.update(get_protocol_driver().get_client_steps())

    def get_selection_steps(self):
        return self._steps['socket_selector']

    def get_reading_steps(self):
        return self._steps['raw_data_reader'] +\
            self._steps['lastrecv_timestamp_updater'] +\
            self._steps['raw_data_normalizer'] +\
            self._steps['heartbeat_receiver'] +\
            self._steps['packet_dispatcher']

    def get_writing_steps(self):
        return self._steps['payload_collector'] +\
            self._steps['heartbeat_sender'] +\
            self._steps['lastsent_timestamp_updater'] +\
            self._steps['packet_data_writer']

    def get_state_check_steps(self):
        return self._steps['state_check']
