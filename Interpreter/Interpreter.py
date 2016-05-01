from AST.Expr import *
from AST.Command import *
from Lexer import *
from Parser import *
import operator

class Interpreter(object):
	def __init__(self):
		self.vars = {}
		self.intops = { "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv }
		self.cmpops = {"==": operator.eq, ">": operator.gt, "<": operator.lt, "!=": operator.ne}

	def run(self):
		while True:
			try:
				text = input('mpr> ')
			except EOFError:
				break;
			tst = Lexer(text)
			prs = Parser(tst)
			try:
				self.interpret(prs.parse())
			except ValueError as err:
				print(err)
			except SyntaxError as err:
				print(err)

	def evalIntExpr(self, node):
		if isinstance(node, ASTIntNode):
			return node.value
		elif isinstance(node, ASTIdentNode):
			return self.vars[node.value]
		elif isinstance(node, ASTIntOpNode):
			left = self.evalIntExpr(node.left)
			right = self.evalIntExpr(node.right)
			return self.intops[node.op](left, right)
		else:
			return 0

	def evalCompareExp(self, node):
		if isinstance(node.left, ASTIntNode):
			left = node.left.value
		elif isinstance(node.left, ASTIdentNode):
			left = self.vars[node.left.value]
		if isinstance(node.right, ASTIntNode):
			right = node.right.value
		elif isinstance(node.right, ASTIdentNode):
			right = self.vars[node.right.value]

		return self.cmpops[node.op](left, right)
	
	def typeCheck(self, old, new):
		if type(old) != type(new):
			raise TypeError('Type mismatch')

	def interpret(self, nodes):
		for node in nodes:
			if isinstance(node, ASTVAR):
				value = self.evalIntExpr(node.value)
				if node.identifier in self.vars.keys():
					self.typeCheck(self.vars[node.identifier], value)				
				self.vars[node.identifier] = value
			elif isinstance(node, ASTPrint):
				if node.type == INT:
					print(node.value)
				elif node.type == IDENT:
					print(self.vars[node.value])
			elif isinstance(node, ASTCmpOpNode):
				print(self.evalCompareExp(node))

