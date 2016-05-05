#Reserved words
VAR, PRINT, IF, ELIF, ELSE = "VAR", "PRINT", "IF", "ELIF", "ELSE"
#Operations
ADDOP, MULOP, CMPOP, BOOLOP = "ADDOP", "MULOP", "CMPOP", "BOOLOP"
#Terminals
INT, IDENT = "INT", "IDENT"
#Special characters
INT, BRACKETL, BRACKETR, COMPOUNDL, COMPOUNDR, EQUALS, SQUARER, SQUAREL = "INT", "LB", "RB", "CL", "CR", "EQUALS", "SR", "SL"
#EOX
EOF, EOC = "EOF", "EOC"

class Token(object):
	def __init__(self, type, value):
		self.type = type
		self.value = value
	def __str__(self):
		return "Token <{type}, {value}>".format(type=self.type, value=self.value)
	def __repr__(self):
		return self.__str__()

