#!/usr/bin/env python

import socket
import SocketServer
import sys
from random import randint
import time
import json

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

json_str = {"ID": "5", "IP": "192.168.1.207", "OPERATION": "READINGS", "reading": "1"}
send("192.168.1.102", 1337, json.dumps(json_str))
