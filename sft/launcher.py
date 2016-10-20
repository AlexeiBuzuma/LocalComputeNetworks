#!/usr/bin/env python3
import logging
import argparse
import sys

from sft.server import SFTServer


def _parse_args():
    parser = argparse.ArgumentParser(
        description='Socket File Transmitter Server')
    parser.add_argument('--host', help='server_ip:server_port')
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Log debug info')
    proto_group = parser.add_mutually_exclusive_group()
    proto_group.add_argument(
        '--tcp', action="store_true",
        help='Use TCP protocol for communication (default)')
    proto_group.add_argument(
        '--udp', action="store_true",
        help='Use UDP protocol for communication')
    args = parser.parse_args()

    if args.host is not None:
        temp_host = args.host.split(':')
        temp_host[1] = int(temp_host[1])
        args.host = tuple(temp_host)

    if args.tcp is False and args.udp is False:
        args.tcp = True

    return args


def main():
    try:
        args = _parse_args()

        log_level = logging.INFO
        if args.verbose is True:
            log_level = logging.DEBUG

        logging.basicConfig(
            stream=sys.stdout,
            level=log_level,
            format='%(asctime)s:%(levelname)s %(message)s')
        LOG = logging.getLogger(__name__)

        LOG.info('Application started')

        if args.tcp is True:
            server_proto = 'TCP'
        elif args.udp is True:
            server_proto = 'UDP'

        server = SFTServer(server_proto, args.host)
        server.run()
    except Exception as e:
        LOG.exception('Unhandled exception is caught')
        LOG.error('Congratulations, application has crashed')
    finally:
        LOG.info('Application terminated')


if __name__ == '__main__':
    main()
