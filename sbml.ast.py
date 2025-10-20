# Name: Kevin Lin SBUID:116145453
# Propositional Logic Grammar

# AST Nodes for Expression Evaluator 

global_names = {}
   
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
				print("SEMANTIC ERROR")
        
		# Multiplication Op Eval 
		elif self.op == "*":
			# Multiplication can be for int or real
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
				return left_val * right_val
			else: 
				print("SEMANTIC ERROR")
        
    	# Division Op Eval
		elif self.op == "/":
			# Division can be for Integers or real
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
				#DNE, Division by 0 is illegal.
				if(right_val == 0):
					print("SEMANTIC ERROR")
				return float(left_val) / float(right_val)
			else:
				print("SEMANTIC ERROR")
    
    	# Integer Division Eval
		elif self.op == "div":
			# Integer Division requires a and b to be integers.
			if isinstance(left_val, (int)) and isinstance(right_val, (int)):
				if(right_val == 0):
					print("SEMANTIC ERROR")
				else:
					return left_val // right_val
			else:
				print("SEMANTIC ERROR")
    
		# Modulus Op Eval
		elif self.op == "%":
			# Modulus can be for Integers
			if isinstance(left_val, (int)) and isinstance(right_val, (int)):
				return left_val%right_val
			else:
				print("SEMANTIC ERROR")
    
		# Addition Op Eval
		elif self.op == "+":
		# Addition operator can be for Integers, real, strings, and lists
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) or\
   			isinstance(left_val, (str)) and isinstance(right_val, (str)) or\
          	isinstance(left_val, (list)) and isinstance(right_val, (list)):
				return left_val + right_val
			else:
				print("SEMANTIC ERROR")

		# Subtraction Op Eval
		elif self.op == "-":
			# Subtraction can be for int or real 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
				return left_val - right_val
			else:
				print("SEMANTIC ERROR")

		# Membership Op Eval
		elif self.op == "in":
			# Membership require b of, a in b, to be String or a List
			if isinstance(right_val, (str, list)):
				return left_val in right_val
			else:
				print("SEMANTIC ERROR")

		# Cons Op Eval
		elif self.op == "::":
			# Cons requires b of, a in b, to be a List
			if isinstance(right_val, (list)):
				# Left will be turned into a list object then use + to combine the two list object.
				return [left_val] + right_val
			else:
				print("SEMANTIC ERROR")
    
		# Boolean Conjunction (AND) Op Eval
		elif self.op == "andalso":
			# left and right must be Booleans
			if isinstance(left_val, (bool)) and isinstance(right_val, (bool)):
				return left_val and right_val
			else:
				print("SEMANTIC ERROR")
    
    	# Boolean Disjunction (OR) Op Eval
		elif self.op == "andalso":
			# Left and Right must be Booleans
			if isinstance(left_val, (bool)) and isinstance(right_val, (bool)):
				return left_val or right_val
			else:
				print("SEMANTIC ERROR")
    
		# Less Than Comparisons
		elif self.op == "<":
			# int, real or strings 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) or\
       			isinstance(left_val, (str)) and isinstance(right_val, (str)):
				return left_val < right_val
			else:
				print("SEMANTIC ERROR")
        
		# Less Than or equal Comparisons
		elif self.op == "<=":
			# int, real or strings 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) or\
       			isinstance(left_val, (str)) and isinstance(right_val, (str)):
				return left_val <= right_val
			else:
				print("SEMANTIC ERROR")
	    
		# Equal Comparisons
		elif self.op == "==":
			# int, real or strings 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) or\
       			isinstance(left_val, (str)) and isinstance(right_val, (str)):
				return left_val == right_val
			else:
				print("SEMANTIC ERROR")
        
		# Greater Than Comparisons
		elif self.op == ">":
			# int, real or strings 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) or\
       			isinstance(left_val, (str)) and isinstance(right_val, (str)):
				return left_val > right_val
			else:
				print("SEMANTIC ERROR")
        
		# Greater Than or equal Comparisons
		elif self.op == ">=":
			# int, real or strings 
			if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)) or\
       			isinstance(left_val, (str)) and isinstance(right_val, (str)):
				return left_val >= right_val
			else:
				print("SEMANTIC ERROR")
    
	def __str__(self):
		res = "\t" * self.parentCount() + f"BinaryOp(op='{self.op}')"
		res += "\n" + str(self.left)
		res += "\n" + str(self.right)
		return res


class Negation(Node):
	def __init__(self,child):
		super().__init__()
		self.op = 'not'
		self.child = child
		self.child.parent = self
  
	def eval(self, n):
		child_val = self.child.eval(n)
		# the values have to be boolean
		if isinstance(child_val, bool):
			return not child_val
		else:
			print("SEMANTIC ERROR")

	def __str__(self):
		res = "\t" * self.parentCount() + f"Negation('{self.op}')"
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
			print("SEMANTIC ERROR")
		if not isinstance(expr_val, (str, list)):
			print("SEMANTIC ERROR")
		# Try block to avoid errors crashing program when indexing non-existent value.
		try:
			return list[expr_val]
		except IndexError:
			print("SEMANTIC ERROR")
   
	def __str__(self):
		res = "\t" * self.parentCount + "IndexOp"
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
            print("SEMANTIC ERROR")
            raise TypeError("Target of tuple indexing must be a tuple")
        
        # Implementation note was sml starts at index 1 and not 0
        py_index = self.index_num - 1
        
        # Indexing needs a try catch to be safe.
        try:
            return tuple_val[py_index]
        except IndexError:
            print("SEMANTIC ERROR")

    def __str__(self):
        res = "\t" * self.parentCount() + f"TupleIndexOp(index={self.i_index})"
        res += "\n" + str(self.expr)
        return res