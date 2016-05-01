INT, ADDOP, MULOP, EOF, LEFTB, RIGHTB = "INT", "ADDOP", "MULOP", "EOF", "LB", "RB"
VAR, IDENT, EQUALS, EOC, PRINT = "VAR", "IDENT", "EQUALS", "EOC", "PRINT"
CMPOP = "CMPOP"

class Token(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value
	def __str__(self):
		return "Token <{type}, {value}>".format(type=self.type, value=self.value)
	def __repr__(self):
		return self.__str__()

class Lexer(object):
	def __init__(self, expr):
		self.expression = expr
		self.position = 0
		self.current_char = self.expression[0]

	def advance(self):
		self.position = self.position + 1
		if self.position >= len(self.expression):
			self.current_char = None
		else:
			self.current_char = self.expression[self.position]

	def is_addop(self):
		return self.current_char == '+' or self.current_char == '-'

	def is_mulop(self):
		return self.current_char == '*' or self.current_char == '/'
	def is_boolop(self):
		result = self.current_char == '<' or self.current_char == '>'
		result = result or (self.expression[self.position] == '=' and self.expression[self.position + 1] == '=')
		result = result or (self.expression[self.position] == '!' and self.expression[self.position + 1] == '=')
		result = result or (self.expression[self.position] == '&' and self.expression[self.position + 1] == '&')
		result = result or (self.expression[self.position] == '|' and self.expression[self.position + 1] == '|') 
		return result
		
	def whitespace(self):
		while self.current_char is not None and self.current_char.isspace():
			self.advance()

	def integer(self):
		result = 0
		while self.current_char is not None and self.current_char.isnumeric():
			result = result*10 + int(self.current_char)
			self.advance()
		return result
	
	def identifier(self):
		result = ""
		while self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
			result += self.current_char
			self.advance()
		if result.upper() == VAR:
			return Token(VAR, None)
		elif result.upper() == PRINT:
			return Token(PRINT, None)
		else:
			return Token(IDENT, result)
	
	def boolop(self):
		op = ""
		result = None
		while self.current_char == '=' or self.current_char == '!' or self.current_char == '&' or self.current_char == '|':
			op = op + self.current_char
			self.advance()
		if op != "":
			result = Token(CMPOP, op)
		else:
			result = Token(CMPOP, self.current_char)
			self.advance()
		return result

	def is_end(self):
		return self.current_char is None
	
	def peak(self):
		position = self.position
		tok = self.get_next_token()
		self.position = position
		return tok
			
	def get_next_token(self):
		self.whitespace()

		if self.current_char is None:
			tok = Token(EOF, None)
		elif self.current_char.isnumeric():
			return Token(INT, self.integer())
		elif self.current_char.isalpha():
			return self.identifier()
		elif self.is_boolop():
			return self.boolop()
		elif self.is_addop():
			tok = Token(ADDOP, self.current_char)
		elif self.is_mulop():
			tok = Token(MULOP, self.current_char)	
		elif self.current_char == '(':
			tok = Token(LEFTB, '(')
		elif self.current_char == ')':
			tok = Token(RIGHTB, ')')
		elif self.current_char == ';':
			tok = Token(EOC, None)
		elif self.current_char == '=':
			tok = Token(EQUALS, '=')
		else:
			raise ValueError('Invalid character encountered')
		self.advance()
		return tok