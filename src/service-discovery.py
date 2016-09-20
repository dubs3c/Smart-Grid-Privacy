from core import Core

class ServiceDiscovery(Core):
	def __init__(self):
		self.node_list = {}

	def listen(self):
		""" Listens on port 1338 for incomming service discovery messages """
		pass

	def broadcast(self):
		pass

	def set_node(self, node):
		pass

	def get_nodes(self):
		return self.node_listt