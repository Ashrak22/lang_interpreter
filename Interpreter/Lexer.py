from Token import *
#Reserved words
VAR, PRINT, IF, ELIF, ELSE, FOR, WHILE = "VAR", "PRINT", "IF", "ELIF", "ELSE", "FOR", "WHILE"
#Operations
ADDOP, MULOP, CMPOP, BOOLOP = "ADDOP", "MULOP", "CMPOP", "BOOLOP"
#Terminals
INT, IDENT = "INT", "IDENT"
#Special characters
INT, BRACKETL, BRACKETR, COMPOUNDL, COMPOUNDR, EQUALS, SQUARER, SQUAREL = "INT", "LB", "RB", "CL", "CR", "EQUALS", "SR", "SL"
#EOX
EOF, EOC = "EOF", "EOC"

RESERVED_WORDS = {
	VAR		: Token(VAR, "var"),
	PRINT	: Token(PRINT, "print"),
	IF		: Token(IF, "if"),
	ELIF	: Token(ELIF, "elif"),
	ELSE	: Token(ELSE, "else"),
	FOR		: Token(FOR, "for"),
	WHILE	: Token(WHILE, "while")
	}

SPECIAL_CHAR_LIST = [';', '(', ')', '{', '}', '[', ']', '=', '+', '-', '*', '/', '<', '>', '!', '&', '|']

SPECIAL_CHARS = {
	';'		: Token(EOC, None),
	'('		: Token(BRACKETL, '('),
	')'		: Token(BRACKETR, ')'),
	'{'		: Token(COMPOUNDL, '{'),
	'}'		: Token(COMPOUNDR, '}'),
	'['		: Token(SQUAREL, '['),
	']'		: Token(SQUARER, ']'),
	'='		: Token(EQUALS, '='),
	'+'		: Token(ADDOP, '+'),
	'-'		: Token(ADDOP, '-'),
	'*'		: Token(MULOP, '*'),
	'/'		: Token(MULOP, '/'),
	'>'		: Token(CMPOP, '>'),
	'>='	: Token(CMPOP, '>='),
	'<'		: Token(CMPOP, '<'),
	'<='	: Token(CMPOP, '<='),
	'=='	: Token(CMPOP, '=='),
	'!='	: Token(CMPOP, '!='),
	'&&'	: Token(BOOLOP, '&&'),
	'||'	: Token(BOOLOP, '||')
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
	
	def specialchars(self):
		op = ""
		result = None
		while self.current_char in SPECIAL_CHAR_LIST:
			op = op + self.current_char
			self.advance()
		return SPECIAL_CHARS[op]

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
		else:
			try:
				 return self.specialchars()
			except Exception as err:
				raise ValueError('Invalid character or operator encountered')