from AST.Expr import *
from AST.Command import *
from Lexer import *
from Parser import *
import operator

class Interpreter(object):
	def __init__(self):
		self.vars = {}
		self.intops = { "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv }
		self.boolops = {"==": operator.eq, ">": operator.gt, "<": operator.lt, "!=": operator.ne}

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

	def evalBoolExp(self, node):
		if isinstance(node.left, ASTIntNode):
			left = node.left.value
		elif isinstance(node.left, ASTIdentNode):
			left = self.vars[node.left.value]
		if isinstance(node.right, ASTIntNode):
			right = node.right.value
		elif isinstance(node.right, ASTIdentNode):
			right = self.vars[node.right.value]

		return self.boolops[node.op](left, right)

	def interpret(self, nodes):
		for node in nodes:
			if isinstance(node, ASTVAR):
				self.vars[node.identifier] = self.evalIntExpr(node.value)
			elif isinstance(node, ASTPrint):
				if node.type == INT:
					print(node.value)
				elif node.type == IDENT:
					print(self.vars[node.value])
			elif isinstance(node, ASTBoolOpNode):
				print(self.evalBoolExp(node))

