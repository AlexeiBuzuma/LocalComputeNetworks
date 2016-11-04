#!/usr/bin/env python3
import logging
import argparse
import sys


def _parse_args():
    parser = argparse.ArgumentParser(
        description='Socket File Transmitter Client')
    parser.add_argument('-s', '--server', help='server_ip:server_port', required=True)
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='Log debug info')
    parser.add_argument('-m', '--mode', dest="mode", help="TCP or UDP mode",
                        choices=["tcp", "udp"], required=True)
    args = parser.parse_args()

    if args.server is not None:
        temp_server = args.server.split(':')
        temp_server[1] = int(temp_server[1])
        args.server = tuple(temp_server)

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
        from sft.client import SFTClient  # don't move to the top!
        client = SFTClient(args.mode, args.server)
        client.run()
    except Exception as e:
        LOG.exception('Unhandled exception is caught')
        LOG.info('Congratulations, application has crashed')
    finally:
        LOG.info('Application terminated')


if __name__ == '__main__':
    main()
