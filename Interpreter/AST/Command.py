class ASTVAR(object):
	def __init__(self, identifier, value):
		self.identifier = identifier
		self.value = value

class ASTPrint(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value