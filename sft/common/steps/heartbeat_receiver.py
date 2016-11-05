import logging

from sft.common.commands.base import CommandIds
from sft.common.utils.packets import get_command_id


LOG = logging.getLogger(__name__)


def heartbeat_receiver(data):
    """Filter heartbeat packages from data flow.

       :param data: [(client_addr, pckt_payload), ... ]
       :return: [(client_addr, pckt_payload), ... ]
    """
    LOG.debug('std heartbeat_receiver step')
    return list(filter(lambda x: get_command_id(x[1]) != CommandIds.HEARTBEAT_COMMAND_ID.value, data))
