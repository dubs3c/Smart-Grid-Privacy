import socket
import threading
import select
import Queue
import json
import colorlog
from crypto import Crypto
from petlib.ec import EcGroup, EcPt
import base64
import time
import msgpack
from petlib import pack

class Core(object):
    """ This class contains core methods used by the application """
    def __init__(self):
        self.port = 1337
        self.host = '0.0.0.0'
        self._callbacks = {}
        self.MAX_RETRIES = 5
        self.nodes = []
        
        self.logger = colorlog.getLogger()
        self.logger.setLevel(colorlog.colorlog.logging.DEBUG)
        self.handler = colorlog.StreamHandler()
        self.handler.setFormatter(colorlog.ColoredFormatter())
        self.logger.addHandler(self.handler)

        '''
        logger.debug("Debug message")
        logger.info("Information message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        '''


    def listen(self):
        cur_thread = threading.current_thread()
        self.logger.debug("Processing listen() in thread: {}".format(cur_thread.name))
        # Create a TCP/IP socket
        sock = None
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(0)
        server_address = (self.host, self.port)
        sock.bind(server_address)
        print("[*] Listening on {}:{}".format(server_address[0],server_address[1]))
        # Allow a backlog of 10 connections
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
                            self.logger.debug('[+] Received {} from {}'.format(data, conn.getpeername()))
                            try:
                                self.parse_operation(data)
                            except:
                                self.logger.error("Some error")
                                conn.close()
                            message_queues[conn].put(data)
                            # Add output channel for response
                            if conn not in wlist:
                                wlist.append(conn)
                        else:
                            # Interpret empty result as closed connection
                            self.logger.debug("[*] Closing {} after receiving no data\n".format(client_address))
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

    def get_pub_keys(self):
        return pub_keys

    def add_pub_key(self,key):
        pub_keys.append(key)

    def send(self, dst, data):
        """ Sends data to specified host
        Args:
            dst (str): The IP address of the host to send to
            data (str): The data to send
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        for tries in range(self.MAX_RETRIES):
            try:
                sock.connect((dst, self.port))
                sock.setblocking(0)
                sock.sendall(data + "\n")
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

    def get_ip(self):
        # This returns 0.0.0.0 which is incorrect.
        return self.host

    def get_nodes(self):
        """ Retrieves the specified IP addresses that should be part of the system network """
        with open('node_list.txt', 'r') as file:
            self.nodes = [line.rstrip('\n') for line in file]

    def parse_operation(self, data):
        """ Parses the OPERATION received from node and executes code based on the OPERATION
        Args:
            data (str): The received data
        """
        json_decoded = json.loads(data)
        op = json_decoded['OPERATION']
        if op in self._callbacks:
            self.logger.debug("Got Operation: " + op)
            self._callbacks[op](json_decoded)
        else:
            self.logger.error("Unknown operation")

    def test_crypto_system(self):
        crypto = Crypto()
        params = crypto.setup()

        message = 100
        msgs = [34,26,75,14,10,10,10] #159

        pub_keys = []
        priv_keys = []
        keypairs = []
        for x in xrange(1,5):
            p = crypto.setup()
            #print("key {}: {}\n").format(x,crypto.key_gen(p))
            keypairs.append(crypto.key_gen(p))

        for s in range(len(keypairs)):
            #print("Pub: {}").format(keypairs[s][0])
            pub_keys.append(keypairs[s][1])
            priv_keys.append(keypairs[s][0])

        group_key = crypto.groupKey(params, pub_keys)

        print("Group key calculated: {}").format(group_key)
        #print("Message to be encrypted: {}").format(message)
        ci = crypto.encrypt(params, group_key, message)

        cis =  []
        for msg in msgs:
            if not cis:
                cis.append(crypto.encrypt(params, group_key, msg))
            else:
                c1 = crypto.encrypt(params, group_key, msg)
                c3 = crypto.add(params, group_key, cis[0], c1)
                cis[0] = c3

        print("cis: {}").format(cis)

        print("Ciphertext: {}").format(ci)

        t1 = crypto.partialDecrypt(params, priv_keys[0], cis[0], False)
        t2 = crypto.partialDecrypt(params, priv_keys[1], t1, False)
        t3 = crypto.partialDecrypt(params, priv_keys[2], t2, False)
        t4 = crypto.partialDecrypt(params, priv_keys[3], t3, True)

        print("Plaintext: {}").format(t4)

