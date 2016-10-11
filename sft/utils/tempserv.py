#!/usr/bin/env python
import socket
import select
import time


def main():
    service_sock = socket.socket()
    service_sock.bind(('localhost', 9899))
    service_sock.listen(10)
    # client_sock, client_addr = service_sock.accept()

    inputs = [service_sock]
    outputs = []

    while True:
        print('iterate')
        readable, writable, exceptional = select.select(
            inputs, outputs, inputs)
        for sock in exceptional:
            inputs.remove(sock)
            if sock in outputs:
                outputs.remove(sock)
            sock.close()
        for sock in readable:
            if sock == service_sock:
                client_sock, client_addr = service_sock.accept()
                print('%s:%d is connected' % client_addr)
                inputs.append(client_sock)
            else:
                data = sock.recv(1024)
                print(data)
                sock.close()
        time.sleep(0.2)


if __name__ == '__main__':
    main()
