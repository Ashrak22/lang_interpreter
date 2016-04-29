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
			result = self.expr()
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
			root = ASTIntOpNode(result, op, self.mulop())
			return root
		return result
	

	def expr(self):
		result = self.mulop()
		root = None
		if self.current_token.type == ADDOP:
			op = self.current_token.value
			self.eat(ADDOP)
			root = ASTIntOpNode(result, op, self.expr())
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
			return ASTVAR(name, self.expr())
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
	
	def boolexpr(self):
		if self.current_token.type == IDENT:
			left = ASTIdentNode(self.current_token.value)
			self.eat(IDENT)
		else:
			left = ASTIntNode(self.current_token.value)
			self.eat(INT)
		
		op = self.current_token.value
		self.eat(BOOLOP)
		
		if self.current_token.type == IDENT:
			right = ASTIdentNode(self.current_token.value)
			self.eat(IDENT)
		else:
			right = ASTIntNode(self.current_token.value)
			self.eat(INT)
		return ASTBoolOpNode(left, op, right)

	def parse(self):
		roots = []
		while not self.lexer.is_end():
			if self.current_token.type == VAR:
				roots.append(self.setvar())
			elif self.current_token.type == PRINT:
				roots.append(self.print())
			elif self.current_token.type == INT and (self.lexer.peak().type == MULOP or self.lexer.peak().type == ADDOP):
				roots.append(self.expr())
			elif (self.current_token.type == INT or self.current_token.type == IDENT) and (self.lexer.peak().type == BOOLOP):
				roots.append(self.boolexpr())
			elif self.current_token.type == IDENT:
				roots.append(self.setvar())
			self.eat(EOC)
		return roots