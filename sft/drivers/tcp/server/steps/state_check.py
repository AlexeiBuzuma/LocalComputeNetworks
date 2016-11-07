import logging

from sft.server.steps import steps as server_steps


LOG = logging.getLogger(__name__)


# def state_check(sockets):
#     LOG.debug('tcp state_check step')
#     # ToDo: Implement tcp server state_check logics

state_check = server_steps['state_check'][0]
