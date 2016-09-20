from core import Core
from petlib.ec import EcGroup
from random import randint

class Client(Core):
	def __init__(self):
		self.core = Core()

	def setup(self):
		"""Generates the Cryptosystem Parameters."""
		G = EcGroup(nid=713)
		g = G.hash_to_point(b"g")
		h = G.hash_to_point(b"h")
		o = G.order()
		return (G, g, h, o)

	def generate_readings(self):
		reading = randint(0,9)
		return reading

	def generate_keys(self, params):
		""" Generate a private / public key pair """
		(G, g, h, o) = params

		priv = o.random() 
		pub = priv * g
		return (priv, pub)


c = Client()
params = c.setup()
priv, pub = c.generate_keys(params)

c.generate_readings()

json_string = '{"id": "2", "IP":"'+c.core.get_ip()+'", "operation": "something","pub":"'+str(pub)+'"}'
c.core.send("localhost", json_string)