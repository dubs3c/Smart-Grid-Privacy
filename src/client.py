from core import Core
from petlib.ec import EcGroup, EcPt
from petlib import pack
from random import randint
from crypto import Crypto
import time, msgpack, json
import base64

clients = ["192.168.1.7","0.0.0.0"]

class Client(Core):
	id = 2
	def __init__(self):
		self.core = Core()

	def generate_readings(self):
		reading = randint(0,9)
		print(time.ctime(),reading)
		enc = crypto.encrypt(params, pub, reading)
		json_str = {"id": c.id, "IP": c.core.get_ip(), "operation": "readings","pub": pub.__dict__, "reading": reading}
		c.core.send("localhost", json.dumps(json_str))

c = Client()
for x in clients:
	if(x == c.core.get_ip):
		c.id = id
		id += 1

crypto = Crypto()
params = crypto.setup()
priv, pub = crypto.key_gen(params)

b64_enc = base64.b64encode(pack.encode(pub))
print b64_enc

c.core.send("localhost", json.dumps({"id":str(c.id), "IP":c.core.get_ip(), "operation": "key", "pub":b64_enc}))

while True:
  c.generate_readings()
  time.sleep(2)
