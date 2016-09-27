from core import Core
from petlib.ec import EcGroup, EcPt
from random import randint
from crypto import Crypto
import time, threading, msgpack
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
		json_string = '{"id": "'+str(c.id)+'", "IP":"'+c.core.get_ip()+'", "operation": "readings","pub":"'+str(pub)+'", "reading": "'+str(reading)+'", "encrypted": "'+str(enc)+'"}'
		c.core.send("localhost", json_string)

c = Client()
for x in clients:
	if(x == c.core.get_ip):
		c.id = id
		id += 1

crypto = Crypto()
params = crypto.setup()
priv, pub = crypto.key_gen(params)

packed = msgpack.packb(pub, default=crypto.default, use_bin_type=True)

c.core.send("localhost", '{"id":"'+str(c.id)+'", "IP":"'+c.core.get_ip()+'", "operation": "key", "pub":"'+packed+'"}')

while True:
  c.generate_readings()
  time.sleep(2)
