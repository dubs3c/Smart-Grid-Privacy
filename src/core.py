import socket, SocketServer, json, colorlog, time, threading, msgpack, base64
from crypto import Crypto
from petlib.ec import EcGroup, EcPt
from petlib import pack

pub_keys = []
clients = []

class MyTCPHandler(SocketServer.BaseRequestHandler):
    pub_keys = []
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    allow_reuse_address=True

    def handle(self):
        # self.request is the TCP socket connected to the client
        print "Client connected with ", self.client_address
        self.data = self.request.recv(1024).strip()
        
        crypto = Crypto()
        params = crypto.setup()
        
        parsed_json = json.loads(self.data)
        if(parsed_json['operation'] == "key"):
            if parsed_json['id'] not in clients:
                pub_keys.append(pack.decode(base64.b64decode(parsed_json['pub'])))
                print("pub keys: {}").format(pub_keys)
                clients.append(parsed_json['id'])
                print("Clients: {}, Pub keys len: {}").format(len(clients),len(pub_keys))
            if len(pub_keys) == 2:
                print("generate group key")
                group_key = crypto.groupKey(params, pub_keys)
                print("group_key: {}").format(group_key)

        if(parsed_json['operation'] == "readings"):
            print(str(parsed_json['id'])+' '+str(parsed_json['IP'])+' '+str(parsed_json['reading']))

        # do_some_logic_with_data(self.data)

        #print "{} wrote:".format(self.client_address[0])
        #print self.data
        #self.request.sendall(self.data.upper()+"\n")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class Core(object):
    """ This class contains core methods used by the application """
    def __init__(self):
        self.port = 1337
        self.host = '0.0.0.0'
        
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

    def get_pub_keys(self):
        return pub_keys

    def add_pub_key(self,key):
        pub_keys.append(key)

    def listen(self):
        """ Creates a listening socket """
        while True:
            try:
                server = ThreadedTCPServer(('',self.port), MyTCPHandler)
                self.logger.info("[*] Server Listening on %s:%d" % (self.host, self.port))
                server.serve_forever()
            except SocketServer.socket.error as exc:
                if exc.args[0] != 48:
                    raise
                self.logger.warning("Port %d is already in use, incrementing port" % (self.port))
                self.port += 1
            else:
                break

    def send(self, dst, data):
        """ Sends data to specified host
        Args:
            dst (str): The IP address of the host to send to
            data (str): The data to send
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock.connect((dst, self.port))
            sock.sendall(data + "\n")
        finally:
            sock.close()

    def get_operation(self, data):
        """ Parses the OPERATION received from node and executes code based on the OPERATION
        Args:
            data (str): The received data
        """
        pass

    def get_ip(self):
        return self.host

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

