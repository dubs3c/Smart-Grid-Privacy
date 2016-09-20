from core import Core

class Client(Core):
    def __init__(self):
    	self.core = Core()

	def generate_readings(self):
		pass

	def generate_keys(self):
		pass


c = Client()

json_string = '{"first_name": "Guido", "last_name":"Rossum"}'
c.core.send("localhost", json_string)