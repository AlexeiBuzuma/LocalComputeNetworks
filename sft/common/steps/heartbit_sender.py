import logging


LOG = logging.getLogger(__name__)


def heartbit_sender(data):
    """Add heartbit packages to data flow.

       :param data: [(client_addr, pckt_payload), ... ]
       :return: [(client_addr, pckt_payload), ... ]
    """
    LOG.debug('std heartbit_sender step')

    # ToDo: Implement heartbit addition
    return data
