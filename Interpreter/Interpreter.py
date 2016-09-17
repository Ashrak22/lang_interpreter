from AST.Expr import *
from AST.Command import *
from Lexer import *
from Parser import *
import operator

class Interpreter(object):
	def __init__(self):
		self.globals = {}
		self.depth = 0
		self.ops = { "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv, "==": operator.eq, ">": operator.gt, "<": operator.lt, "!=": operator.ne, "<=": operator.le, ">=": operator.ge }

	def run(self):
		tst = Lexer("")
		prs = Parser(tst)
		
		while True:
			try:
				compound = 0
				tst.flush()
				text = ""
				descend = False;
				text = input('mpr> ')
				if '{' in text:
					descend = True;
					compound += 1
				while compound > 0 or (text != "" and text[-1] != ';' and text[-1] != '}'):
					inpt = input('... ')
					if '{' in inpt:
						descend = True;
						compound += 1
					if '}' in inpt:
						compound -= 1
					text += inpt
			except EOFError:
				break;
			tst.append(text)
			try:
				self.interpret(descend, prs.compound())
			except ValueError as err:
				print(err)
			except SyntaxError as err:
				print(err)
			except TypeError as err:
				print(err)
			except KeyError as err:
				print("Variable {var} not defined!".format(var=err))

	def evalIntExpr(self, node):
		if isinstance(node, ASTIntNode):
			return node.value
		elif isinstance(node, ASTIdentNode):
			return self.globals[node.value]
		elif isinstance(node, ASTExpNode):
			left = self.evalIntExpr(node.left)
			right = self.evalIntExpr(node.right)
			self.typeCheck(left, right)
			if node.op == "&&":
				self.typeCheck(left, True)
				return left and right
			elif node.op == "||":
				self.typeCheck(left, True)
				return left or right
			else:
				self.typeCheck(left, 1)
				return self.ops[node.op](left, right)
		else:
			return 0

	def evalIf(self, node):
		value = self.evalIntExpr(node.condition)
		self.typeCheck(value, True)
		if value:
			self.interpret(True, node.true)
		else:
			if isinstance(node.false, ASTIF):
				self.evalIf(node.false)
			else:
				self.interpret(True, node.false)
	
	def evalWhile(self, node):
		condition = self.evalIntExpr(node.condition)
		self.typeCheck(condition, True)
		while condition:
			self.interpret(True, node.body)
			condition = self.evalIntExpr(node.condition)
	
	def evalFor(self, node):
		nodes = []
		nodes.append(node.init)
		self.interpret(False, nodes)
		condition = self.evalIntExpr(node.condition)
		while condition:
			self.interpret(True, node.body)
			nodes = []
			nodes.append(node.step)
			self.interpret(False, nodes)
			condition = self.evalIntExpr(node.condition)

	def typeCheck(self, old, new):
		if type(old) != type(new):
			raise TypeError('Type mismatch')

	def interpret(self, descend, nodes):
		if(descend):
			scope = self.getCurrentScope()
			scope['locals'] = {}
			self.depth += 1
		for node in nodes:
			if isinstance(node, ASTVAR):
				value = self.evalIntExpr(node.value)
				localscope = self.getCurrentScope()
				if not node.new:
					self.typeCheck(localscope[node.identifier], value)
					localscope[node.identifier] = value;
				else:
					self.getCurrentScope()[node.identifier] = value
			elif isinstance(node, ASTPrint):
				if node.type == INT:
					print(node.value)
				elif node.type == IDENT:
					print(self.getScopeByVar(node.value)[node.value])
			elif isinstance(node, ASTIF):
				self.evalIf(node)
			elif isinstance(node, ASTWhile):
				self.evalWhile(node)
			elif isinstance(node, ASTFor):
				self.evalFor(node)
		if(self.depth >= 0 and descend):
			self.depth -= 1
			scope = self.getCurrentScope()
			scope.pop('locals')

	def getCurrentScope(self):
		res = self.globals
		for i in range(self.depth):
			res = res['locals']
		return res;

	def getScopeByVar(self, identifier):
		scope = self.globals
		res = None;

		if identifier in scope.keys():
				res = scope;

		for i in range(self.depth):
			scope = scope['locals']
			if identifier in scope.keys():
				res = scope;
			
		return res;
