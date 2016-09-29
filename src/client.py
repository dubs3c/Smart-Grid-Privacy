from core import Core
from petlib.ec import EcGroup, EcPt
from petlib import pack
from random import randint
from crypto import Crypto
import time, msgpack, json
import base64

class Client(Core):

    def __init__(self):
        super(Client, self).__init__()
        self.id = randint(1000,100000)
        self.logger.info("Running in Client mode")
        self.public_keys = []
        self.client_keypair = []
        self.clients = ["192.168.1.7","0.0.0.0"]

    def generate_readings(self):
        reading = randint(0,9)
        print(time.ctime(),reading)
        crypto = Crypto()
        params = crypto.setup()
        enc = crypto.encrypt(params, self.client_keypair[1], reading)
        json_str = {"id": self.id, "IP": self.get_ip(), "operation": "readings","pub": self.client_keypair[1].__dict__, "reading": reading}
        self.send("localhost", json.dumps(json_str))

    def add_public_key(self,key):
        self.public_keys.append(key)

    def get_public_keys(self, key):
        return self.public_keys

    def setup(self):
        self.logger.debug("Generating keypairs...")
        crypto = Crypto()
        params = crypto.setup()
        priv, pub = crypto.key_gen(params)
        self.client_keypair.extend([priv, pub])
        self.add_public_key(pub)

    def start(self):
        
        #self.logger.debug("Listening")
        #self.listen()
        for x in self.clients:
            if(x == self.get_ip):
                self.id = id
                id += 1

        b64_enc = base64.b64encode(pack.encode(self.client_keypair[1]))
        self.send("localhost", json.dumps({"id":str(self.id), "IP":self.get_ip(), "operation": "key", "pub":b64_enc}))
        self.logger.debug("Key has been sent")
        while True:
            self.generate_readings()
            time.sleep(2)

'''
c = Client()
c.listen()
for x in clients:
    if(x == c.get_ip):
        c.id = id
        id += 1

crypto = Crypto()
params = crypto.setup()
priv, pub = crypto.key_gen(params)

b64_enc = base64.b64encode(pack.encode(pub))
print b64_enc

c.send("localhost", json.dumps({"id":str(c.id), "IP":c.get_ip(), "operation": "key", "pub":b64_enc}))

while True:
  c.generate_readings()
  time.sleep(2)
'''

