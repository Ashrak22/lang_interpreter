from Lexer import *
from AST.Expr import *
from AST.Command import *

class Parser(object):
	def __init__(self, lexer):
		self.lexer = lexer
		self.current_token = lexer.get_next_token()

	def eat(self, type):
		if self.current_token.type == type:
			self.current_token = self.lexer.get_next_token()
		else:
			raise ValueError("Found {found}. Expected {token}".format(found=self.current_token.type, token=type))
		
	def term(self):
		if self.current_token.type == LEFTB:
			self.eat(LEFTB)
			result = self.boolop()
			self.eat(RIGHTB)
		elif self.current_token.type == IDENT:
			result = ASTIdentNode(self.current_token.value)
			self.eat(IDENT)
		else:
			result = ASTIntNode(self.current_token.value)
			self.eat(INT)
		return result

	def mulop(self):
		result = self.term()
		root = None
		if self.current_token.type == MULOP:
			op = self.current_token.value
			self.eat(MULOP)
			root = ASTExpNode(result, op, self.mulop())
			return root
		return result
	

	def expr(self):
		result = self.mulop()
		root = None
		if self.current_token.type == ADDOP:
			op = self.current_token.value
			self.eat(ADDOP)
			root = ASTExpNode(result, op, self.expr())
			return root
		return result

	def cmpop(self):
		result = self.expr()
		root = None
		if self.current_token.type == CMPOP:
			op = self.current_token.value
			self.eat(CMPOP)
			root = ASTExpNode(result, op, self.cmpop())
			return root
		return result

	def boolop(self):
		result = self.cmpop()
		root = None
		if self.current_token.type == BOOLOP:
			op = self.current_token.value
			self.eat(BOOLOP)
			root = ASTExpNode(result, op, self.boolop())
			return root
		return result

	def setvar(self):
		create = False
		if self.current_token.type == VAR:
			create = True
			self.eat(VAR)

		name = self.current_token.value
		self.eat(IDENT)

		if self.current_token.type == EOC and create:
			return ASTVAR(name, None)
		elif self.current_token.type == EQUALS:
			self.eat(EQUALS)
			return ASTVAR(name, self.boolop())
		else:
			raise SyntaxError('Wrong Syntax')

	def print(self):
		self.eat(PRINT)
		self.eat(LEFTB)
		if self.current_token.type == IDENT:
			name = self.current_token.value
			self.eat(IDENT)
			self.eat(RIGHTB)
			return ASTPrint(IDENT, name)

	def parse(self):
		roots = []
		while not self.lexer.is_end():
			if self.current_token.type == VAR:
				roots.append(self.setvar())
			elif self.current_token.type == PRINT:
				roots.append(self.print())
			elif self.current_token.type == INT and (self.lexer.peak().type == MULOP or self.lexer.peak().type == ADDOP):
				roots.append(self.expr())
			elif self.current_token.type == IDENT:
				roots.append(self.setvar())
			self.eat(EOC)
		return roots