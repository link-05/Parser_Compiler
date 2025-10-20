# Name: Kevin Lin SBUID:116145453
#Tokens and expression rules for evaluating expression

import ply.lex as lex

tokens = (
    'INT', 'REAL', 'BOOL', 'STRING', 'LIST',
    'LEFTPAREN', 'RIGHTPAREN',
    'EXP', 'TIMES', 'DIV', 'INTDIV',
    'MOD', 'PLUS', 'MINUS', 'CONS',
    'MEMBERSHIP', 'BOOLCONJUGATION', 'BOOLNEG',
    'BOOLDISJUNCTION', 'LESSTHAN', 'LESSTHANOREQUAL',
    'EQUALS', 'NOTEQUALS', 'GREATERTHAN', 'GREATERTHANOREQUAL',
    'INDEXAT', 'INDEXOP'
)
''' All tokens are Integer, Real, Boolean, String, List, Left Parenthesis, Right Parenthesis
Exponent, Times, Divide, Int Divide, Modulus, Plus, Minus, Cons, Membership, Boolean Conjugation,
Boolean Negation, Boolean Disjunction, Less than, Less than or equal, Equals equal,
Not Equal, Greater Than, Greater than, Greater than or equal, #i (tuple) <- IndexAt, A[B] Index operation.

Above are the tokens that are for all the existing data type, operations, and 
Additionally all the operations that can be done exist in the token as well'''

# Tokens Matching Declaration (ALL TOKENS MUST HAVE A MATCHING DECLARATION OF t_whateverTheTokenWas)
t_ignore = ' \t'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_STRING = r'[a-zA-Z_]*'
t_LEFTPAREN = r'\(' 
t_RIGHTPAREN = r'\)'
t_TIMES = r'\*' 
t_DIV = r'div' 
t_MOD = r'mod'
t_LESSTHAN = r'\<' 
t_EQUALS = r'\=\='
t_NOTEQUALS = r'\!\=' 
t_GREATERTHAN = r'\>' 
t_LIST = r'\[\]'

#These are the operations that are used for when special action code must be executed. 
def t_CONS(t):
   pass
def t_EXP(t):
   pass
def t_INTDIV(t):
   pass
def t_NUMBERS(t):
   pass
def t_BOOL(t):
   pass
def t_MEMBERSHIP(t):
    pass
def t_REAL(t):
    pass
def t_BOOLNEG(t):
   pass
def t_BOOLDISJUNCTION(t):
   pass
def t_BOOLCONJUGATION(t):
   pass
def t_INDEXAT(t):
   pass
def t_INDEXOP(t):
   pass

#These opera