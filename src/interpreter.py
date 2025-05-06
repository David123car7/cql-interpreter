import csv
from parser import Parser

class Interpreter:
    def __init__(self):
        self.parser = Parser()
    
    def run(self, data):
        result = self.parser.parse(data)
        if result is None:
            print("No result from parser")
            return None
        
        self.execute(result)
    
    def execute(self, command):
        cmd = command[0]
        if(cmd == "IMPORT"):
            print(f"Executing command: {command}")
            self.read_csv(command[2])

    def read_csv(self, filename):
            if(filename == ""):
                print("Filename is empty")
                return None

            try:
                data = []
                header = None

                with open(filename, "r", newline="") as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if row and row[0].startswith("#"):
                            continue

                        # First line is the header
                        if header is None:
                            header = row
                        else:
                            data.append(row)
                print(header)
                print(data)
                return {"header": header, "data": data}
            except Exception as e:
                print(f"Error reading CSV file: {str(e)}")
                return None
