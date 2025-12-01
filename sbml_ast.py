# Name: Kevin Lin SBUID:116145453
# Propositional Logic Grammar

# AST Nodes for Expression Evaluator 
	
# Below Node definition is taken from the sample PLY Parsing Files
class Node():
	def __init__(self):
		self.parent = None
	def parentCount(self):
		count = 0
		current = self.parent
		while current is not None:
			count += 1
			current = current.parent 
		return count
# The node classes that I will need are
# Number - Int/Float, Boolean, String, List, Tuple 
# Those are the datatypes as given in SBML Description

# One for all operator (all in the from a op b)
# Negation
# Index for Indexing Operation
# TupleIndex for tuple Indexing Operation

#Number nodes (Definitions from ply_demo_ast.py file)
class Int(Node):
	def __init__(self, v):
		super().__init__()
		self.value = int(v)

	def eval(self, n):
		return self.value
	
	def __str__(self):
		res = "\t" * self.parentCount() + f"Int({str(self.value)})" 
		return res

class Real(Node):
	def __init__(self, v):
		super().__init__()
		self.value = float(v)

	def eval(self, n):
		return self.value

	def __str__(self):
		res = "\t" * self.parentCount() + f"Real({str(self.value)})"
		return res
	
class Boolean(Node):
	def __init__(self, v):
		super().__init__()
		self.value = v

	def eval(self, n):
		return self.value

	def __str__(self):
		res = "\t" * self.parentCount() + f"Boolean({str(self.value)})"
		return res

class String(Node):
	def __init__(self, v):
		super().__init__()
		self.value = v
	
	def eval(self, n):
		return self.value
	
	def __str__(self):
		res = "\t" * self.parentCount() + f"String('{self.value}')"
		return res

class List(Node):
	def __init__(self, elements):
		super().__init__()
		# A list has a set of elements and each element needs to be processed for parents as well
		self.elements = elements
		for element in elements:
			element.parent = self
	
	def eval(self, n):
		#Evaluate expression for each element 
		return [element.eval(n) for element in self.elements]
	
	def __str__(self):
		res = "\t" * self.parentCount() + "List"
		# Add every element in the list into the result.
		for element in self.elements:
			res += "\n" + str(element)
		return res
	
class Tuple(Node):
	def __init__(self, elements):
		super().__init__()
		# A list has a set of elements and each element needs to be processed for parents as well
		self.elements = elements
		for element in elements:
			element.parent = self
	
	def eval(self, n):
		#Evaluate expression for each element 
		return tuple(element.eval(n) for element in self.elements)
	
	def __str__(self):
		res = "\t" * self.parentCount() + "Tuple"
		# Add every element in the list into the result.
		for element in self.elements:
			res += "\n" + str(element)
		return res
	
# Majority of the operators are binary operations
# Similar init, Variated eval, similar __str__
# PLY documentation - combined rules

class BinaryOp(Node):
	def __init__(self, left, op, right):
		super().__init__()
		self.left = left
		self.right = right
		self.op = op
		self.left.parent = self
		self.right.parent = self 
	
	def eval(self, n):
		left_val = self.left.eval(n)
		right_val = self.right.eval(n)
		# Operator check for what happens.
	
		# Exponentiation Op Eval
		if self.op == "**":
			# Exponentiation operator can be for Integers or real
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
				return left_val ** right_val
			else:
				# Type Mismatches
				raise Exception
		
		# Multiplication Op Eval 
		elif self.op == "*":
			# Multiplication can be for int or real
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
				return left_val * right_val
			else: 
				raise Exception
		
		# Division Op Eval
		elif self.op == "/":
			# Division can be for Integers or real
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
				#DNE, Division by 0 is illegal.
				if(right_val == 0):
					raise Exception
				return float(left_val) / float(right_val)
			else:
				raise Exception
	
		# Integer Division Eval
		elif self.op == "div":
			# Integer Division requires a and b to be integers.
			if isinstance(left_val, (int)) and isinstance(right_val, (int))\
				and not isinstance(left_val, (bool)) and not isinstance(right_val, (bool)):
				if(right_val == 0):
					raise Exception
				else:
					return left_val // right_val
			else:
				raise Exception
	
		# Modulus Op Eval
		elif self.op == "mod":
			# Modulus can be for Integers
			if isinstance(left_val, (int)) and isinstance(right_val, (int)):
				return left_val % right_val
			else:
				raise Exception
	
		# Addition Op Eval
		elif self.op == "+":
			# Case 1: Number addition (explicitly excluding booleans)
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) and \
				not isinstance(left_val, bool) and not isinstance(right_val, bool):
				return left_val + right_val
			elif isinstance(left_val, str) and isinstance(right_val, str):
				return left_val + right_val
			elif isinstance(left_val, list) and isinstance(right_val, list):
				return left_val + right_val
			else:
				raise Exception

		# Subtraction Op Eval
		elif self.op == "-":
			# Subtraction can be for int or real 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
				return left_val - right_val
			else:
				raise Exception

		# Membership Op Eval
		elif self.op == "in":
			# Membership require b of, a in b, to be String or a List
			if isinstance(right_val, (str, list)):
				return left_val in right_val
			else:
				raise Exception

		# Cons Op Eval
		elif self.op == "::":
			# Cons requires b of, a in b, to be a List
			if isinstance(right_val, (list)):
				# Left will be turned into a list object then use + to combine the two list object.
				return [left_val] + right_val
			else:
				raise Exception
	
		# Boolean Conjunction (AND) Op Eval
		elif self.op == "andalso":
			# left and right must be Booleans
			if isinstance(left_val, (bool)) and isinstance(right_val, (bool)):
				return left_val and right_val
			else:
				raise Exception
	
		# Boolean Disjunction (OR) Op Eval
		elif self.op == "orelse":
			# Left and Right must be Booleans
			if isinstance(left_val, (bool)) and isinstance(right_val, (bool)):
				return left_val or right_val
			else:
				raise Exception
	
		# Less Than Comparisons
		elif self.op == "<":
			# int, real or strings 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) or\
					isinstance(left_val, (str)) and isinstance(right_val, (str)):
				return left_val < right_val
			else:
				raise Exception
		
		# Less Than or equal Comparisons
		elif self.op == "<=":
			# int, real or strings 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) or\
					isinstance(left_val, (str)) and isinstance(right_val, (str)):
				return left_val <= right_val
			else:
				raise Exception
		
		# Equal Comparisons
		elif self.op == "==":
			# int, real, list/tuple or strings 
			return left_val == right_val

		elif self.op == '<>':
			return left_val != right_val

		# Greater Than Comparisons
		elif self.op == ">":
			# int, real or strings 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) or\
					isinstance(left_val, (str)) and isinstance(right_val, (str)):
				return left_val > right_val
			else:
				raise Exception
		
		# Greater Than or equal Comparisons
		elif self.op == ">=":
			# int, real or strings 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) or\
					isinstance(left_val, (str)) and isinstance(right_val, (str)):
				return left_val >= right_val
			else:
				raise Exception
	
	def __str__(self):
		res = "\t" * self.parentCount() + f"BinaryOp(op='{self.op}')"
		res += "\n" + str(self.left)
		res += "\n" + str(self.right)
		return res


class UnaryOp(Node):
	def __init__(self, op, child):
		super().__init__()
		self.op = op
		self.child = child
		self.child.parent = self
	
	def eval(self, n):
		child_val = self.child.eval(n)
	
		if self.op == '-':
			return -1 * child_val

		# the values have to be boolean
		elif self.op == 'not':
			if isinstance(child_val, bool):
				return not child_val
			else:
				raise Exception
		else:
			raise Exception

	def __str__(self):
		res = "\t" * self.parentCount() + f"UnaryOp(op='{self.op}')"
		res += "\n" + str(self.child)
		return res
	
class IndexOp(Node):
	def __init__(self, list, i_expr):
		super().__init__()
		# a is a list
		self.list = list
		# b is an expression that will be the index
		self.i_expr = i_expr
		self.list.parent = self
		self.i_expr.parent = self
		
	def eval(self, n):
		list_val = self.list.eval(n)
		expr_val = self.i_expr.eval(n)

		if not isinstance(list_val, (str, list)):
			raise TypeError("Target for indexing [] must be a list or string")
			
		# FIX: The index must be an integer, but NOT a boolean
		if not isinstance(expr_val, int) or isinstance(expr_val, bool):
			raise TypeError("Index must be an integer")
			
		try:
			return list_val[expr_val]
		except IndexError:
			raise IndexError("Index out of bounds")
	
	def __str__(self):
		res = "\t" * self.parentCount() + "IndexOp"
		res += "\n" + str(self.list)
		res += "\n" + str(self.i_expr)
		return res

class TupleIndexOp(Node):
	def __init__(self, i_index, tuple_expr):
		super().__init__()
		self.i_index = i_index 
		self.expr = tuple_expr # This is a node
		self.expr.parent = self

	def eval(self, n):
		tuple_val = self.expr.eval(n)
		
		if not isinstance(tuple_val, tuple):
			raise Exception
		
		# Implementation note was sml starts at index 1 and not 0
		py_index = self.i_index - 1
		
		# Indexing needs a try catch to be safe.
		try:
			return tuple_val[py_index]
		except IndexError:
			raise Exception

	def __str__(self):
		res = "\t" * self.parentCount() + f"TupleIndexOp(index={self.i_index})"
		res += "\n" + str(self.expr)
		return res

class ID(Node):
	def __init__(self, n):
		super().__init__()
		self.name = n
	
	def eval(self, n):
		if self.name in n:
			return n[self.name]
		else:
			raise Exception()	
	def __str__(self):
		res = "\t" * self.parentCount() + f"Variable('{self.name}')"
		return res
	
#Statements
	
# Block Statement - Any expressions or statements enclosed by {}
class Block(Node):
	def __init__(self, statements):
		super().__init__()
		self.statements = statements
		for statement in statements:
			statement.parent = self
	
	def eval(self, n):
		for statement in self.statements:
			statement.eval(n)
	
	def __str__(self):
		res = "\t" * self.parentCount() + "Block"
		for statement in self.statements:
			res += "\n" + str(statement)
		return res

# Assignment has two types here, simple variable assignment and list reassignment
class Assignment(Node):
	def __init__(self, target, value_expr):
		super().__init__()
		self.target = target # ID or IndexOP
		self.value_expr = value_expr
		self.target.parent = self
		self.value_expr.parent = self
	
	def eval(self, n):
		value = self.value_expr.eval(n)
		# Assignment
		if isinstance(self.target, ID):
			n [self.target.name] = value
		# Index Assignment for list
		elif isinstance(self.target, IndexOp):
			list_val = self.target.list.eval(n)
			index_val = self.target.i_expr.eval(n)
			# Indexing can only be with final outcome integer, 
				#	if its a list or boolean, clearly wrong if otherwise.
			if not isinstance(list_val, list):
				raise Exception()
			if isinstance(index_val, list) or isinstance(index_val, bool):
				raise Exception()
			# # allow negative index but not out of bound index.
			# if abs(index_val) >= len(list.val):
			# 	raise Exception()

			# Do assignment once safe
			list_val[index_val] = value
		else:
			raise Exception()
	def __str__(self):
		res = "\t" * self.parentCount() + "Assignment"
		res += "\n" + str(self.target)
		res += "\n" + str(self.value_expr)
		return res

# Print is just print
class Print(Node):
	def __init__(self, expr):
		super().__init__()
		self.expr = expr
		self.expr.parent = self
	def eval(self, n):
		# Eval expression. Print expression.
		value = self.expr.eval(n)
		print(value)
	def __str__(self):
		res = "\t" * self.parentCount() + "Print"
		res += "\n" + str(self.expr)
		return res

#If statement will be 3 parts:
#	the condition part,
#	the then part, and
#	a boolean for 
#		if there is an attached else statement.
class If(Node):
	def __init__(self, condition, then_block, else_block = None):
		super().__init__()
		self.condition = condition
		self.then_block = then_block
		self.else_block = else_block
		self.condition.parent = self
		self.then_block.parent = self
		if else_block:
			self.else_block.parent = self
	def eval(self, n):
		# Eval the condition expression
		condition_val = self.condition.eval(n)
		# res from condition must be t/f
		if not isinstance(condition_val, bool):
			raise Exception()
		# If true, eval then block
		if condition_val:
			self.then_block.eval(n)
		# If false, eval else block
		elif self.else_block:
			self.else_block.eval(n)

	def __str__(self):
		res = "\t" * self.parentCount() + "If"
		res += "\n" + str(self.condition)
		res += "\n" + str(self.then_block)
		if self.else_block:
			res += "\n" + str(self.else_block)
		return res

# While loop statement, will hold a condition and body block 
class While(Node):
	def __init__(self, condition, body):
		self.condition = condition
		self.body = body
		self.condition.parent = self
		self.body.parent = self
	
	def eval(self, n):
		while True:
			condition_val = self.condition.eval(n)
			
			# Condition must eval to a boolean
			if not isinstance(condition_val, bool):
				raise Exception()

			# If false, break
			if not condition_val:
				break
			
			# If true, eval the body
			self.body.eval(n)
	
	def __str__(self):
		res = "\t" * self.parentCount() + "While"
		res += "\n" + str(self.condition)
		res += "\n" + str(self.body)
		return res
class Program(Node):
	# Program Node contains the functions and main code block
	def __init__(self, functions, main):
		super().__init__()
		self.functions = functions
		self.main = main
		for fun in functions:
			fun.parent = self
		self.main.parent = self
	
	def eval(self, n):
		# Need a table to store all function definitions
		fun_table = {}
		for fun_def in self.functions:
			fun_table[fun_def.name] = fun_def
			   
		#Store into table n
		n['__functions__'] = fun_table

		#After functions are stored globally - allow the main block to execute
		self.main.eval(n)

	def __str__(self):
		res = "\t" * self.parentCount() + "Program"
		for fun in self.functions:
			res += "\n" + str(fun)
		res += "\n" + str(self.main)
		return res

class FunctionDef(Node):
	# Function Defintion 
	def __init__(self, name, params, body, ret_expr):
		super().__init__()
		self.name = name
		self.params = params
		self.body = body
		self.ret_expr = ret_expr
		self.body.parent = self
		self.ret_expr.parent = self
		
	# This is only the definition/holder for all the requirements
	def eval(self, n):
		pass

	def __str__(self):
		res = "\t" * self.parentCount() + f"FunctionDef(name='{self.name}', params={self.params})"
		res += "\n" + str(self.body)
		res += "\n" + str(self.ret_expr)
		return res
	
class FunctionCall(Node):
	# Function call expression
	def __init__(self, name, args):
		super().__init__()
		self.name = name
		self.args = args
		for arg in args:
			arg.parent = self
	def eval(self, n):
		# Get table, check for function name, extract func def
		if '__functions__' not in n:
			raise Exception
		# Use special naming to avoid overwriting when a function name called functions exist
		fun_table = n['__functions__']

		if self.name not in fun_table:
			raise Exception
		
		func_def = fun_table[self.name]


		arg_values = []
		for arg in self.args:
			arg_values.append(arg.eval(n))

		if len(arg_values) != len(func_def.params):
			raise Exception()
		
		# Need scope to prevent memory overwriting in n
		#   when same func is called during recursion.
		scope = {'__functions__': fun_table}

		# Copy parameter (var to its value) for the local scope 
		# zip pairs up element from separate lists returned as a list of pairs
		for param_name, arg_value in zip(func_def.params, arg_values):
			scope[param_name] = arg_value

		# Run the function body
		func_def.body.eval(scope)

		return func_def.ret_expr.eval(scope)
	
	def __str__(self):
		res = "\t" * self.parentCount() + f"FunctionCall(name= '{self.name}')"
		for arg in self.args:
			res += "\n" + str(arg)
		return res