class ASTVAR(object):
	def __init__(self, identifier, value, new):
		self.identifier = identifier
		self.value = value
		self.new = new 

class ASTPrint(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value

class ASTIF(object):
	def __init__(self, condition, true, false):
		self.condition = condition
		self.true = true
		self.false = false

class ASTWhile(object):
	def __init__(self, condition, body):
		self.condition = condition
		self.body = body

class ASTFor(object):
	def __init__(self, init, condition, step, body):
		self.init = init
		self.condition = condition
		self.step = step
		self.body = body
