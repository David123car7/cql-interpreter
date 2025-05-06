from lexer import Lexer
from parser import Parser
import sys

lexer = Lexer()
parser = Parser()

class Interpreter:
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as file:
            contents = file.read()
            result = parser.parse(contents)
            print(result)
    else:
        print("Usage: python interpreter.py <filename>")
        sys.exit(1)



