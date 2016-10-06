from core import Core
from crypto import Crypto
import json
from petlib import pack
import base64
import time
import msgpack
import json
import colorlog
import sys
import threading

class Server(Core):
    """ Server class """
    def __init__(self):
        # By doing this we automatically inherit the variables and methods of the parent class, without needing to initiate first
        super(Server, self).__init__()
        self.id = 1
        self.logger.info("Running in Server mode")
        self.public_keys = []
        self.test = []
        self.server_keypair = []

    def add_public_key(self,key):
        self.public_keys.append([key])

    def get_public_keys(self, key):
        return self.public_keys

    def genereate_keys(self):
        ''' Generate cryptographic keypairs '''
        crypto = Crypto()
        params = crypto.setup()
        priv, pub = crypto.key_gen(params)

        self.core.add_pub_key(pub)

    def setup(self):
        # Create necessary callbacks
        self._callbacks["GROUP_KEY_CREATE"] = self._compute_group_key
        self._callbacks["DECRYPT_GROUP_FINAL"] = self._decrypt_group_final
        self._callbacks["READINGS"] = self._track_readings

        self.get_nodes()
        crypto = Crypto()
        params = crypto.setup()
        priv, pub = crypto.key_gen(params)
        self.server_keypair.extend([priv, pub])
        self.add_public_key(pub)

    def start(self):
        listening_thread = threading.Thread(target=self.listen)
        try:
            listening_thread.start()
        except (KeyboardInterrupt, SystemExit):
            cleanup_stop_thread();
            sys.exit()

    def _compute_group_key(self,json_decoded):
        pub_keys = []
        clients = []

        crypto = Crypto()
        params = crypto.setup()
        print("Print len of pubkeys is: {}".format(len(self.test)))
        if json_decoded['ID'] not in clients:
            print(pack.decode(base64.b64decode(json_decoded['PUB'])))
            self.test.append(pack.decode(base64.b64decode(json_decoded['PUB'])))
            print("pub keys: {}").format(self.test)
            clients.append(json_decoded['ID'])
            print("Clients: {}, Pub keys len: {}").format(len(clients),len(self.test))
        if len(self.test) == 2:
            print("generate group key")
            group_key = crypto.groupKey(params, self.test)
            print("group_key: {}").format(group_key)

    def _decrypt_group_final(self,json_decoded):
        pass

    def _track_readings(self,json_decoded):
        pass


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