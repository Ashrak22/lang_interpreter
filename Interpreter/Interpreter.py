from AST.Expr import *
from AST.Command import *
from Lexer import *
from Parser import *
import operator

class Interpreter(object):
	def __init__(self):
		self.globals = {}
		self.ops = { "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv, "==": operator.eq, ">": operator.gt, "<": operator.lt, "!=": operator.ne, "<=": operator.le, ">=": operator.ge }

	def run(self):
		tst = Lexer("")
		prs = Parser(tst)
		
		while True:
			try:
				compound = 0
				tst.flush()
				text = ""
				text = input('mpr> ')
				if '{' in text:
					compound += 1
				while compound > 0 or (text != "" and text[-1] != ';' and text[-1] != '}'):
					inpt = input('... ')
					if '{' in inpt:
						compound += 1
					if '}' in inpt:
						compound -= 1
					text += inpt
			except EOFError:
				break;
			tst.append(text)
			try:
				self.interpret(prs.compound())
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
			self.interpret(node.true)
		else:
			if isinstance(node.false, ASTIF):
				self.evalIf(node.false)
			else:
				self.interpret(node.false)
	
	def evalWhile(self, node):
		condition = self.evalIntExpr(node.condition)
		self.typeCheck(condition, True)
		while condition:
			self.interpret(node.body)
			condition = self.evalIntExpr(node.condition)

	def typeCheck(self, old, new):
		if type(old) != type(new):
			raise TypeError('Type mismatch')
	
	def evalFor(self, node):
		localvars = {}

		init = node.init


	def interpret(self, nodes):
		for node in nodes:
			if isinstance(node, ASTVAR):
				value = self.evalIntExpr(node.value)
				if node.identifier in self.globals.keys():
					self.typeCheck(self.globals[node.identifier], value)				
				self.globals[node.identifier] = value
			elif isinstance(node, ASTPrint):
				if node.type == INT:
					print(node.value)
				elif node.type == IDENT:
					print(self.globals[node.value])
			elif isinstance(node, ASTIF):
				self.evalIf(node)
			elif isinstance(node, ASTWhile):
				self.evalWhile(node)
			elif isinstance(node, ASTFor):
				self.evalFor(node)

