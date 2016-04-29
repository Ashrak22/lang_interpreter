class ASTIntNode(object):
	def __init__(self, value):
		self.value = value

class ASTIdentNode(object):
	def __init__(self, value):
		self.value = value

class ASTIntOpNode(object):
	def __init__(self, left, op, right):
		self.right = right
		self.op = op
		self.left = left
		

class ASTBoolNode(object):
	def __init__(self, left, op, right):
		self.right = right
		self.op = op
		self.left = left