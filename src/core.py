import socket
import SocketServer
import json
import colorlog
from crypto import Crypto

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    allow_reuse_address=True

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()

        parsed_json = json.loads(self.data)
        print(parsed_json['id']+' '+parsed_json['IP'])

        # do_some_logic_with_data(self.data)

        #print "{} wrote:".format(self.client_address[0])
        #print self.data
        #self.request.sendall(self.data.upper()+"\n")

class Core:
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
 
    def listen(self):
        """ Creates a listening socket """
        while True:
            try:
                server = SocketServer.TCPServer((self.host, self.port), MyTCPHandler)
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

        pub_keys = []
        for x in xrange(1,5):
            p = crypto.setup()
            # print("key {}: {}\n").format(x,crypto.key_gen(p))
            pub_keys.append(crypto.key_gen(p))
        
        group_key = crypto.groupKey(params, pub_keys)

        #print("Public keys: {}\n").format(pub_keys)
        print("Group key calculated: {}\n").format(group_key)

        ci = crypto.encrypt(params, group_key, 99)
        print("{}\n").format(ci)


