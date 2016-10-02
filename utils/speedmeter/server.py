#!/usr/bin/env python3
import socket
import sys
import time


def start_server():
    server_sock = socket.socket()
    server_addr = ("192.168.10.1", 9999)
    server_sock.bind(server_addr)
    print('Starting server on %s:%d' % server_addr)
    server_sock.listen(10)
    conn_id = 0

    while True:
        client_sock, client_addr = server_sock.accept()
        print('Started downloading from %s:%d' % client_addr)
        byte_counter = 0
        conn_id += 1
        f = open('file.out.' + str(conn_id), 'wb')

        start_time = time.time()
        l = client_sock.recv(1024)
        while (l):
            f.write(l)
            byte_counter += len(l)
            l = client_sock.recv(1024)
        end_time = time.time()

        f.close()
        client_sock.close()

        speed = byte_counter / (end_time - start_time) / 125000
        print('    File downloaded, average speed %f Mbit' % speed)
    server_sock.close()

if __name__ == '__main__':
    try:
        start_server()
    except KeyboardInterrupt as e:
        print('Terminating server')
