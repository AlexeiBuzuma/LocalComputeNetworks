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
    parser.add_argument("-m", dest="mode", help="TCP or UDP mode",
                        choices=["tcp", "udp"], required=True)
    args = parser.parse_args()

    if args.host is not None:
        temp_host = args.host.split(':')
        temp_host[1] = int(temp_host[1])
        args.host = tuple(temp_host)

    return args


def main():
    args = _parse_args()
    log_level = logging.INFO
    if args.verbose is True:
        log_level = logging.DEBUG

    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format='%(asctime)s:%(levelname)s %(message)s')
    LOG = logging.getLogger(__name__)

    try:
        LOG.info('Application started')
        server = SFTServer(args.mode, args.host)
        server.run()
    except Exception as e:
        LOG.exception('Unhandled exception is caught')
        LOG.info('Congratulations, application has crashed')
    finally:
        LOG.info('Application terminated')


if __name__ == '__main__':
    main()
