# Name: Kevin Lin SBUID:116145453
import sys

import sbml_parser

def main():
	flagCall = sys.argv[1]
	filename = sys.argv[2]
	try:
		with open(filename, 'r') as file:
			for line in file:
				line = line.strip()
				if not line:
					continue
				try:
					ast_root = sbml_parser.parser.parse(line, lexer=sbml_parser.lexer)
					if ast_root is None:
						print("SYNTAX ERROR")
						continue
					if flagCall == '-P':
						print(str(ast_root))
					elif flagCall == '-E':
						names = {} 
						result = ast_root.eval(names)
						if isinstance(result, str):
							print(f"'{result}'") # Strings must be in single quotes
						else:
							print(result)
				except SyntaxError as e:
					print("SYNTAX ERROR")
				except Exception as e:
					print("SEMANTIC ERROR")
	except FileNotFoundError:
		print(f"Error: Input file '{filename}' not found.")
		sys.exit(1)
  
  
if __name__ == "__main__":
	main()
	
		
