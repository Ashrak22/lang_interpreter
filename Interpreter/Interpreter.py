from AST.Expr import *
from AST.Command import *
from Lexer import *
from Parser import *

class Interpreter(object):
	def __init__(self):
		self.vars = {}

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
			if node.op == '+':
				return left + right
			elif node.op == '-':
				return left - right
			elif node.op == '*':
				return left * right
			elif node.op == '/':
				return left / right
			else:
				raise TypeError('Wrong Node Type')
		else:
			return 0

	def interpret(self, nodes):
		for node in nodes:
			if isinstance(node, ASTVAR):
				self.vars[node.identifier] = self.evalIntExpr(node.value)
			elif isinstance(node, ASTPrint):
				if node.type == INT:
					print(node.value)
				elif node.type == IDENT:
					print(self.vars[node.value])

