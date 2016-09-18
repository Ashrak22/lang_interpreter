class Scope(object):
	def __init__(self):
		self.vars = {}
		self.depth = 0

	def getCurrentScope():
		res = self.vars
		for i in range(self.depth):
			res = res['locals']
		return res

	def getScopeByVars():
		scope = self.vars
		res = None;

		if identifier in scope.keys():
				res = scope;

		for i in range(self.depth):
			scope = scope['locals']
			if identifier in scope.keys():
				res = scope;
			
		return res;

	def descend():
		scope = self.getCurrentScope()
		scope['locals'] = {}
		self.depth += 1

	def ascend():
		if self.depth > 0:
			self.depth -= 1
			scope = self.getCurrentScope()
			scope.pop('locals')

class Namespace(object):
	def __init__(self, name):
		self.scope = Scope()
		self.name = name

