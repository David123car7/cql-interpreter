from interpreter import Interpreter
import sys

class Main:
    interpreter = Interpreter()

    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], "r") as file:
                contents = file.read()
                result = interpreter.run(contents)
        except Exception as e:
            print(e)    
    else:
        for expr in iter(lambda: input(">> "), ""):
            try:
                result = interpreter.run(expr)
            except Exception as e:
                print(e)



