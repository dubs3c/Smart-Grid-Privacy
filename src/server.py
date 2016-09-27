from core import Core
from crypto import Crypto
import json

class Server(Core):
    """ Server class """
    def __init__(self):
        self.core = Core()
        self.id = 1
        
	def get_pub_key(self):
		return pub

s = Server()
crypto = Crypto()
params = crypto.setup()
priv, pub = crypto.key_gen(params)

s.core.add_pub_key(pub)

s.core.listen()

#if len(s.core.get_pub_keys) == 2:
#	print("group key")
#	group_key = crypto.groupKey(params, s.core.get_pub_keys)
#s.core.test_crypto_system()