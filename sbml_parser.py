# Name: Kevin Lin SBUID:116145453
#Tokens and expression rules for evaluating expression

import ply.lex as lex
import ply.yacc as yacc
import sbml_ast

 # From PLY DOC
reserved_keywords = {
	'True' : 'TRUE',
	'False' : 'FALSE',
	'div' : 'DIV',
	'mod' : 'MOD',
	'in' : 'IN',
	'not' : 'NOT',
	'andalso' : 'ANDALSO',
	'orelse' : 'ORELSE'
}

# PLY DOC technique for reserved keyword token = [] + list()

tokens = [
	'INT', 'REAL', 'STRING', 'ID',
	'LEFTPAREN', 'RIGHTPAREN', 'LEFTBRACKET', 'RIGHTBRACKET', 'COMMA',
	'EXP', 'TIMES', 'DIVIDE', 'PLUS', 'MINUS', 'CONS', 'LESSTHAN', 'LESSTHANOREQUALS',
	'EQUALS', 'NOTEQUALS', 'GREATERTHAN', 'GREATERTHANOREQUALS', 'TUPLEINDEX'
 ] + list(reserved_keywords.values())
''' All tokens are Integer, Real, Boolean, String, List, Left Parenthesis, Right Parenthesis
Exponent, Times, Divide, Int Divide, Modulus, Plus, Minus, Cons, Membership, Boolean Conjugation,
Boolean Negation, Boolean Disjunction, Less than, Less than or equal, Equals equal,
Not Equal, Greater Than, Greater than, Greater than or equal, #i (tuple) <- IndexAt, A[B] Index operation.

Above are the tokens that are for all the existing data type, operations, and List/Tuple tokens
Additionally all the operations that can be done exist in the token as well'''
def t_EXP(t):
	r'\*\*'
	return t
def t_CONS(t):
	r'::'
	return t

def t_LESSTHANOREQUALS(t):
	r'<='
	return t
def t_GREATERTHANOREQUALS(t):
	r'>='
	return t
def t_EQUALS(t):
	r'=='
	return t
def t_NOTEQUALS(t):
	r'<>'
	return t
def t_LESSTHAN(t):
	r'<'
	return t
def t_GREATERTHAN(t):
	r'>'
	return t


# Single char Tokens Matching Declaration (ALL TOKENS MUST HAVE A MATCHING DECLARATION OF t_whateverTheTokenWas)
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'/'
t_TIMES = r'\*' 
t_TUPLEINDEX = r'\#'

t_LEFTPAREN = r'\(' 
t_RIGHTPAREN = r'\)'
t_LEFTBRACKET = r'\['
t_RIGHTBRACKET = r'\]'
t_COMMA = r'\,'

#These are the operations that are used for when special action code must be executed. 
def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = reserved_keywords.get(t.value, 'ID')
	if t.type == 'TRUE':
		t.value = True
	elif t.type == 'FALSE':
		t.value = False
	return t

def t_REAL(t):
	#Need to match, 
	# 		0 or more digit with decimal and 1 or more digit
	#		decimal and 1 or more digit possibly with e or E of - or + value digit/s
	#		optional decimal e or E
	#		optional no decimal e or E
	r'(\d+\.\d*|\.\d+)([eE][-+]?\d+)?|\d+[eE][-+]?\d+'
	t.value = float(t.value)
	return t
def t_INT(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_STRING(t):
	r'\"[^\"]*\"|\'[^\']*\''
	t.value = t.value[1:-1]
	return t

# From PLY DOC
t_ignore = ' \t'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)
	
def t_error(t):
	t.lexer.skip(1)
	raise SyntaxError
	# raise SyntaxError(t.value)
	
lexer = lex.lex()

# Parsing Rule
precedence = (
	('left', 'ORELSE'),
	('left', 'ANDALSO'),
	('left', 'NOT'),
	('left', 'LESSTHAN', 'LESSTHANOREQUALS', 'EQUALS', 'NOTEQUALS', 'GREATERTHANOREQUALS', 'GREATERTHAN'),
	('right', 'CONS'),
	('left', 'IN'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE', 'DIV', 'MOD'),
	('right', 'EXP'),
	('left', 'TUPLEINDEX'),
	('left', 'LEFTBRACKET', 'RIGHTBRACKET'),
	('right', 'UMINUS') 
)

# PLY DOC combine grammar rule idea
def p_expression_binaryop(t):
	'''expression : expression EXP expression
				  | expression TIMES expression
				  | expression DIVIDE expression
				  | expression DIV expression
				  | expression MOD expression
				  | expression PLUS expression
				  | expression MINUS expression
				  | expression CONS expression
				  | expression IN expression
				  | expression ANDALSO expression
				  | expression ORELSE expression
				  | expression LESSTHAN expression
				  | expression LESSTHANOREQUALS expression
				  | expression EQUALS expression
				  | expression NOTEQUALS expression
				  | expression GREATERTHANOREQUALS expression
				  | expression GREATERTHAN expression'''
	t[0] = sbml_ast.BinaryOp(t[1], t[2], t[3])

	# From ply_demo.py example file
def p_expression_unary_minus(t):
	'expression : MINUS expression %prec UMINUS'
	# This handles unary minus (e.g., -5 or -(2+3)) [cite: 257]
	# The '%prec UMINUS' tells PLY to use the (high) precedence
	# of 'UMINUS' for this rule, not the (low) precedence of 'MINUS'.
	t[0] = sbml_ast.UnaryOp('-', t[2])
	
def p_expression_unary_not(t):
	'expression : NOT expression'
	# This handles Boolean negation [cite: 312]
	t[0] = sbml_ast.UnaryOp('not', t[2])
 
def p_expression_tuple_index(t):
	'expression : TUPLEINDEX INT LEFTPAREN expression RIGHTPAREN'
	# p2 is the index integer 
	# p4 is the expression that evaluates to a tuple	
	t[0] = sbml_ast.TupleIndexOp(t[2],t[4]) 
 
 # For some reason #3 (4, 3, 2, 1) will not work without directly handing 
 # single parenthesis case so this is to specifically handle this case. 
def p_expression_tuple_index_direct(t):
	'expression : TUPLEINDEX INT LEFTPAREN element_list_comma RIGHTPAREN'
	# This handles #3(4, 3, 2, 1) directly - treating the contents as a tuple
	t[0] = sbml_ast.TupleIndexOp(t[2], sbml_ast.Tuple(t[4]))
 
def p_expression_group(t):
	'expression : LEFTPAREN expression RIGHTPAREN'
	t[0] = t[2]

def p_expression_index(t):
	'expression : expression LEFTBRACKET expression RIGHTBRACKET'
	# a[b]
	t[0] = sbml_ast.IndexOp(t[1], t[3])


 
def p_expression_int(t):
	'expression : INT'
	t[0] = sbml_ast.Int(t[1])

def p_expression_real(t):
	'expression : REAL'
	t[0] = sbml_ast.Real(t[1])
 
# Any other leftover ID
def p_expression_id(t):
	'expression : ID'
	t[0] = sbml_ast.ID(t[1])

def p_expression_string(t):
	'expression : STRING'
	t[0] = sbml_ast.String(t[1])

def p_expression_boolean(t):
	'''expression : TRUE
				  | FALSE'''
	t[0] = sbml_ast.Boolean(t[1])

def p_expression_list(p):
	'expression : LEFTBRACKET optional_element_list RIGHTBRACKET'
	# p[2] list of AST nodes from optional_element_list
	p[0] = sbml_ast.List(p[2])

def p_optional_element_list(p):
	'''optional_element_list : element_list
							 | empty'''
	if p[1] is None:
		p[0] = []  # Empty list
	else:
		p[0] = p[1] # Pass up element_list to AST

def p_element_list(p):
	'''element_list : expression
					| element_list COMMA expression'''
	if len(p) == 2:
		p[0] = [p[1]]  # A list with one element
	else:
		p[0] = p[1] + [p[3]] # A list with more elements

# Tuples 
def p_expression_tuple(p):
	'expression : LEFTPAREN element_list_comma RIGHTPAREN'
	# at least 2 elements.
	p[0] = sbml_ast.Tuple(p[2])

def p_expression_tuple_singleton(p):
	'expression : LEFTPAREN expression COMMA RIGHTPAREN'
	# 1 element
	p[0] = sbml_ast.Tuple([p[2]])

def p_element_list_comma(p):
	'''element_list_comma : expression COMMA expression
                          | element_list_comma COMMA expression'''
	# p[1] is the first element
	# p[3] is the list of remaining elements
	if isinstance(p[1], list):
		# if p1 is a list and p3 is not.
		p[0] = p[1] + [p[3]] 
	else:
		# if p1 p3 are both elements
		p[0] = [p[1], p[3]]
		
def p_empty(p):
	'empty :'
	p[0] = None
	
# From ply_demo.py
def p_error(t):
	raise SyntaxError()
	# raise SyntaxError(t.value)
	
parser = yacc.yacc()