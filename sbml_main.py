# Name: Kevin Lin SBUID:116145453
import sys

import sbml_parser

def main():
	flagCall = sys.argv[1]
	filename = sys.argv[2]
	try:
		with open(filename, 'r') as file:
			text = file.read()
		try:
			# This is an entire program now so not calling parse for each individual line but instead a whole txt of content.
			ast_root = sbml_parser.parser.parse(text, lexer=sbml_parser.lexer)
			if ast_root is None:
				print("SYNTAX ERROR")
				sys.exit(1)
			if flagCall == '-P':
				print(str(ast_root))
			elif flagCall == '-E':
				names = {} 
				result = ast_root.eval(names)
				# if isinstance(result, str):
				# 	print(f"'{result}'") # Strings must be in single quotes
				# else:
				# 	print(result)
		except SyntaxError as e:
			print("SYNTAX ERROR")
			sys.exit(1)
		except Exception as e:
			print("SEMANTIC ERROR")
			sys.exit(1)

	except FileNotFoundError:
		print(f"Error: Input file '{filename}' not found.")
		sys.exit(1)
  
  
if __name__ == "__main__":
	main()
	
		
