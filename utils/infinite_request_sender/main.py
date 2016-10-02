#!/usr/bin/env python3
import argparse
import server
import client


def _get_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", dest="server", help="Run script in server mode", action="store_true")
    parser.add_argument("-c", dest="client", help="Run script in client mode", action="store_true")
    parser.add_argument("-p", dest="port", help="Port for connect", default=9999)
    parser.add_argument("--ip", dest="ip", help="Server ip.")
    parser.add_argument("-d", dest="debug", help="Printing debug message.", action="store_true", default=True)

    return parser.parse_args()


if __name__ == '__main__':
    args = _get_arguments()

    if args.server:
        server.run(port=args.port, debug=args.debug)

    elif args.client:
        client.run(ip=args.ip, port=args.port, debug=args.debug)
