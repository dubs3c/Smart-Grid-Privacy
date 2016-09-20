from core import Core

class Client(Core):
    def __init__(self):
    	self.core = Core()

	def generate_readings(self):
		pass

	def generate_keys(self):
		pass


c = Client()

msg = 'something'
json_string = '{"id": "2", "IP":"'+c.core.get_ip()+'", "operation": "something","data": "'+msg+'"}'
c.core.send("localhost", json_string)