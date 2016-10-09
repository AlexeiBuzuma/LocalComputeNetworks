#!/usr/bin/env python3
import argparse
from server import run_tcp_server, run_udp_server
from client import run_tcp_client, run_udp_client


def _get_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument("-m", dest="mode", help="TCP or UDP mode", choices=["tcp", "udp"], required=True)
    parser.add_argument("-s", dest="server", help="Run script in server mode", action="store_true")
    parser.add_argument("-c", dest="client", help="Run script in client mode", action="store_true")
    parser.add_argument("-p", dest="port", help="Port for connect", default=9999)
    parser.add_argument("--ip", dest="ip", help="Server ip.")
    parser.add_argument("-d", dest="debug", help="Printing debug message.", action="store_true", default=True)

    return parser.parse_args()


def main():
    args = _get_arguments()

    print(args.mode)

    server_runner = run_udp_server if args.mode == "udp" else run_tcp_server
    client_runner = run_udp_client if args.mode == "udp" else run_tcp_client

    if args.server:
        server_runner(port=args.port, debug=args.debug)

    elif args.client:
        client_runner(ip=args.ip, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
