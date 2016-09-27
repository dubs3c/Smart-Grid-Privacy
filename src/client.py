from core import Core
from petlib.ec import EcGroup, EcPt
from random import randint
from crypto import Crypto
import time, threading, msgpack, json
from threading import Timer

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

packed = msgpack.packb(pub, default=crypto.default, use_bin_type=True)
x = msgpack.unpackb(packed, ext_hook=crypto.ext_hook, encoding='utf-8')

assert x == pub

c.core.send("localhost", json.dumps({"id":str(c.id), "IP":c.core.get_ip(), "operation": "key", "pub":pub.__dict__}))

while True:
  c.generate_readings()
  time.sleep(2)
