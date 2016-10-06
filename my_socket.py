#!/usr/bin/env python

import socket
import SocketServer
import select
import Queue
import sys
from random import randint
import time
import threading

def listen(src_port):
    cur_thread = threading.current_thread()
    print("Processing listen() in thread: {}".format(cur_thread.name))
    # Create a TCP/IP socket
    sock = None
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    server_address = ('0.0.0.0', int(src_port))
    sock.bind(server_address)
    print("[*] Listening on {}:{}".format(server_address[0],server_address[1]))
    sock.listen(10)

    # Outgoing message queues (socket:Queue)
    message_queues = {}

    rlist = [sock]
    wlist = []
    xlist = []
    try:
        while True:
            readable, writable, exceptional = select.select(rlist, wlist, xlist, 1)
            for conn in readable:
                if conn is sock:
                    # A "readable" server socket is ready to accept a connection
                    connection, client_address = conn.accept()
                    print("[+] New connection from {}".format(client_address))
                    connection.setblocking(0)
                    rlist.append(connection)
                    message_queues[connection] = Queue.Queue()
                else:
                    data = conn.recv(1024)
                    if data:
                        # A readable client socket has data
                        print('[+] Received {} from {}'.format(data, conn.getpeername()))
                        message_queues[conn].put(data)
                        # Add output channel for response
                        if conn not in wlist:
                            wlist.append(conn)
                    else:
                        # Interpret empty result as closed connection
                        print("[*] Closing {} after receiving no data\n".format(client_address))
                        if conn in wlist:
                            wlist.remove(conn)
                        rlist.remove(conn)
                        conn.close()
                        # Remove message queue
                        del message_queues[conn]

            # # Handle outputs i.e send back data to source
            # for conn in wlist:
            #     try:
            #         next_msg = message_queues[conn].get_nowait()
            #     except Queue.Empty:
            #         # No messages waiting so stop checking for writability.
            #         print >>sys.stderr, 'output queue for', conn.getpeername(), 'is empty'
            #         wlist.remove(s)
            #     else:
            #         print >>sys.stderr, 'sending "%s" to %s' % (next_msg, conn.getpeername())
            #         conn.send(next_msg)

            # # Handle "exceptional conditions"
            # for conn in xlist:
            #     print >>sys.stderr, 'handling exceptional condition for', conn.getpeername()
            #     # Stop listening for input on the connection
            #     inputs.remove(conn)
            #     if conn in wlist:
            #         wlist.remove(s)
            #     conn.close()
            #     # Remove message queue
            #     del message_queues[s]

    except KeyboardInterrupt:
        # Close all sockets when the program is killed
        for sock in rlist:
            sock.close()

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

def generate_readings(dst):
    cur_thread = threading.current_thread()
    print("Processing generate_readings() in thread: {}".format(cur_thread.name))
    while True:
        reading = randint(0,9)
        print(time.ctime(),reading)
        send(dst, 1234, str(reading))
        time.sleep(2)


server_thread = threading.Thread(target=listen, args=(sys.argv[2],))
readings = threading.Thread(target=generate_readings, args=(sys.argv[1],))

server_thread.start()
readings.start()
