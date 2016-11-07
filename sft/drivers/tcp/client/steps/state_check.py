import logging

from sft.client.steps import steps as client_steps


LOG = logging.getLogger(__name__)


# def state_check(sockets):
#     LOG.debug('tcp state_check step')
#     # ToDo: Implement tcp client state_check logics

state_check = client_steps['state_check'][0]
