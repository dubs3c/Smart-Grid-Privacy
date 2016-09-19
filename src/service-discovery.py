from core import Core

class ServiceDiscovery(Core):
	def __init__(self):
		self.node_list = {}

	def listen(self):
		''' Listens on port 1338 for incomming service discovery messages '''
		pass

	def broadcast(self):
		pass

	def setNode(self, node):
		pass

	def getNodes(self):
		return self.node_listt