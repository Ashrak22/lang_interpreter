INT, ADDOP, MULOP, EOF, LEFTB, RIGHTB = "INT", "ADDOP", "MULOP", "EOF", "LB", "RB"
VAR, IDENT, EQUALS, EOC = "VAR", "IDENT", "EQUALS", "EOC"
CMPOP, BOOLOP = "CMPOP", "BOOLOP"
PRINT, IF = "PRINT", "IF"

class Token(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value
	def __str__(self):
		return "Token <{type}, {value}>".format(type=self.type, value=self.value)
	def __repr__(self):
		return self.__str__()

RESERVED_WORDS = {
	VAR : Token(VAR, "var"),
	PRINT : Token(PRINT, "print"),
	IF : Token(IF, "if") 
	}

class Lexer(object):
	def __init__(self, expr):
		self.expression = expr
		self.position = -1
		self.advance()
	
	def append(self, text):
		if self.expression == "":
			self.expression = text
			self.position = self.position-1;
		else:
			self.expression = self.expression + '\r\n' + text
			self.position = self.position+2-1;
		self.advance()
	def flush(self):
		self.position = len(self.expression)
		self.current_char = None
	def advance(self):
		self.position = self.position + 1
		if self.position >= len(self.expression):
			self.position = len(self.expression)
			self.current_char = None
		else:
			
			self.current_char = self.expression[self.position]

	def is_addop(self):
		return self.current_char == '+' or self.current_char == '-'

	def is_mulop(self):
		return self.current_char == '*' or self.current_char == '/'
	def is_cmpop(self):
		result = self.current_char == '<' or self.current_char == '>'
		result = result or (self.expression[self.position] == '=' and self.expression[self.position + 1] == '=')
		result = result or (self.expression[self.position] == '!' and self.expression[self.position + 1] == '=')
		return result
	def is_boolop(self):
		result = (self.expression[self.position] == '&' and self.expression[self.position + 1] == '&')
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
		return RESERVED_WORDS.get(result.upper(), Token(IDENT, result))
	
	def cmpop(self):
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

	def boolop(self):
		op = self.expression[self.position] + self.expression[self.position + 1]
		self.advance()
		self.advance()
		return Token(BOOLOP, op)

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
		elif self.is_cmpop():
			return self.cmpop()
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