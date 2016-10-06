#!/usr/bin/env python

import socket
import threading
import SocketServer
import multiprocessing
from random import randint
import time
import sys

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        print("Processing client {} in thread: {}".format(self.client_address[0],cur_thread.name))
        print("Received readings: {}".format(data))
        #response = "{}: {}".format(cur_thread.name, data)
        #self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def send(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for tries in range(10):
        try:
            sock.connect((ip, port))
            sock.setblocking(0)
            sock.sendall(message)
            #   response = sock.recv(1024)
            #print "Received: {}".format(response)
        except EnvironmentError as exc :
            if exc.errno == errno.ECONNREFUSED:
                time.sleep(5)
            else:
                raise
        else:
            break
        finally:
            sock.close()
            break

def generate_readings(dst):
    while True:
        reading = randint(0,9)
        print(time.ctime(),reading)
        send(dst, 1234, str(reading))
        time.sleep(5)

if __name__ == "__main__":

    HOST, PORT = "0.0.0.0", 1234

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    client_readings = threading.Thread(target=generate_readings, args=(sys.argv[1],))
    # Exit the server thread when the main thread terminates
    #server_thread.daemon = True
    
    server_thread.start()

    # p = multiprocessing.Process(target=generate_readings, args=(sys.argv[1],))
    # p.start()
    # p.join()
    client_readings.start()
    print "Server loop running in thread: ", server_thread.name
    print("Client readings running in thread: {}".format(client_readings.name))
    #server.shutdown()
    #server.server_close()
