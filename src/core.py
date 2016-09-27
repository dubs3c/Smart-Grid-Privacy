import socket
import SocketServer
import json

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
        print(parsed_json['id']+' '+parsed_json['IP']+' '+parsed_json['pub']+' '+parsed_json['reading'])

        # do_some_logic_with_data(self.data)

        #print "{} wrote:".format(self.client_address[0])
        #print self.data
        #self.request.sendall(self.data.upper()+"\n")

class Core:
    """ This class contains core methods used by the application """
    def __init__(self):
        self.port = 1339
        self.host = '0.0.0.0'
 
    def listen(self):
        """ Creates a listening socket """
        while True:
            try:
                server = SocketServer.TCPServer((self.host, self.port), MyTCPHandler)
                print("[*] Server Listening on %s:%d" % (self.host, self.port))
                server.serve_forever()
            except SocketServer.socket.error as exc:
                if exc.args[0] != 48:
                    raise
                print 'Port', self.port, 'already in use'
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

    def generate_keys(self):
        """ Generate private and public keys """
        pass
