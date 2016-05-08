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
			str = "Found {found}. Expected {token}".format(found=self.current_token.type, token=type)
			self.lexer.flush()
			self.current_token = Token(EOF, None)
			raise ValueError(str)
		
	def term(self):
		if self.current_token.type == BRACKETL:
			self.eat(BRACKETL)
			result = self.boolop()
			self.eat(BRACKETR)
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
			root = ASTExpNode(result, op, self.expr())
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
		self.eat(BRACKETL)
		if self.current_token.type == IDENT:
			name = self.current_token.value
			self.eat(IDENT)
			self.eat(BRACKETR)
			return ASTPrint(IDENT, name)

	def compound(self):
		if self.current_token.type == COMPOUNDL:
			result = self.parse()
		else:
			result = self.parse(True)
		return result

	def conditional(self):
		if self.current_token.type == IF:
			self.eat(IF)
		else: 
			self.eat(ELIF)
		condition = self.boolop()
		true = self.compound()
		if self.current_token.type == ELIF:
			false = self.conditional()
		else:
			self.eat(ELSE)
			false = self.compound()
		return ASTIF(condition, true, false)
	
	def whileloop(self):
		self.eat(WHILE)
		condition = self.boolop()
		body = self.compound()
		return ASTWhile(condition, body)
		
	def parse(self, singlec = False):
		roots = []
		if self.current_token.type == EOF:
			self.eat(EOF)
		if not singlec:
			self.eat(COMPOUNDL)
		while not self.lexer.is_end():
			if self.current_token.type == VAR or self.current_token.type == IDENT:
				roots.append(self.setvar())
			elif self.current_token.type == PRINT:
				roots.append(self.print())
			elif self.current_token.type == INT and (self.lexer.peak().type == MULOP or self.lexer.peak().type == ADDOP):
				roots.append(self.expr())
			elif self.current_token.type == IF:
				roots.append(self.conditional())
			elif self.current_token.type == WHILE:
				roots.append(self.whileloop())
			if self.current_token.type == COMPOUNDR:
				self.eat(COMPOUNDR)
				return roots
			else:
				self.eat(EOC)
			if singlec:
				return roots
		self.eat(COMPOUNDR)
		return roots