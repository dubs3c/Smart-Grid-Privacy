from core import Core
import json

class Server(Core):
    """ Server class """
    def __init__(self):
        self.core = Core()

    def hello(self):
        print("test")

    def create_global_key(self):
        pass

s = Server()

s.hello()
s.core.listen()
