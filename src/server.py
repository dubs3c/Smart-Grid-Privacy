from core import Core
import json

class Server(Core):
    """ Server class """
    def __init__(self):
        self.core = Core()

    def hello(self):
        print("test")

    def create_global_key(self, params, pubKeys=[]):
		""" Generate a group public key from a list of public keys """
		(G, g, h, o) = params
		#let pub be equal to the first public key in the list
		pub = pubKeys[0]
		#scan through the rest of the list and add public keys
		for key in pubKeys[1:]:
			pub = pub+key
		return pub

s = Server()

s.hello()
s.core.listen()