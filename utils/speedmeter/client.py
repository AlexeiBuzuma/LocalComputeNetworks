#!/usr/bin/env python3
import socket
import sys

s = socket.socket()
s.connect(("192.168.10.1", 9999))

with open("file.zip", "rb") as f:
    l = f.read(1024)
    while (l):
        s.send(l)
        l = f.read(1024)
s.close()
