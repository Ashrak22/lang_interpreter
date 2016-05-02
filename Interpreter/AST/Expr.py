class ASTIntNode(object):
	def __init__(self, value):
		self.value = value

class ASTIdentNode(object):
	def __init__(self, value):
		self.value = value

class ASTExpNode(object):
	def __init__(self, left, op, right):
		self.right = right
		self.op = op
		self.left = left
		

#class ASTCmpOpNode(object):
#	def __init__(self, left, op, right):
#		self.right = right
#		self.op = op
#		self.left = left