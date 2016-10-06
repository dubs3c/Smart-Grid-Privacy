#!/usr/bin/env python

import socket
import SocketServer
import sys
from random import randint
import time

def send(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for tries in range(5):
        try:
            sock.connect((ip, port))
            sock.setblocking(0)
            sock.sendall(message)
        except EnvironmentError as exc :
            if exc.errno == errno.ECONNREFUSED:
                print("conn refused")
                time.sleep(5)
            else:
                print("nope")
                raise
        else:
            break
        finally:
            sock.close()
            break


send("192.168.1.150", 1234, "This is a test message")