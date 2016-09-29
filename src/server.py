from core import Core
from crypto import Crypto
import json

class Server(Core):
    """ Server class """
    def __init__(self):
        # By doing this we automatically inherit the variables and methods of the parent class, without needing to initiate first
        super(Server, self).__init__()
        self.id = 1
        self.logger.info("Running in Server mode")
        self.public_keys = []
        self.server_keypair = []

    def add_public_key(self,key):
        self.public_keys.append(key)

    def get_public_keys(self, key):
        return self.public_keys

    def genereate_keys(self):
        ''' Generate cryptographic keypairs '''
        crypto = Crypto()
        params = crypto.setup()
        priv, pub = crypto.key_gen(params)

        self.core.add_pub_key(pub)

    def setup(self):
        crypto = Crypto()
        params = crypto.setup()
        priv, pub = crypto.key_gen(params)
        self.server_keypair.extend([priv, pub])
        self.add_public_key(pub)
        self.listen()


'''
s = Server()
crypto = Crypto()
params = crypto.setup()
priv, pub = crypto.key_gen(params)

s.get_public_keys(pub)

s.listen()
'''
#if len(s.core.get_pub_keys) == 2:
#   print("group key")
#   group_key = crypto.groupKey(params, s.core.get_pub_keys)
#s.core.test_crypto_system()