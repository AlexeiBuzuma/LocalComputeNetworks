import logging


LOG = logging.getLogger(__name__)


def heartbeat_sender(data):
    """Add heartbeat packages to data flow.

       :param data: [(client_addr, pckt_payload), ... ]
       :return: [(client_addr, pckt_payload), ... ]
    """
    LOG.debug('std heartbeat_sender step')

    # ToDo: Implement heartbeat addition
    return data
