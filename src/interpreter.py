import csv
from parser import Parser
from filesCSV import FilesCSV

class Interpreter:
    def __init__(self):
        self.parser = Parser()
        self.filesCSV = FilesCSV()
        self.tablesData = {}
        self.filePath = "files/"
        
    
    def run(self, data):
        result = self.parser.parse(data)
        if result is None:
            print("No result from parser")
            return None

        for cmd in result:
            self.execute(cmd)
    
    def execute(self, command):
        cmd = command[0]
        if(cmd == "IMPORT"):
            self.import_table(command[1], command[2])
        elif(cmd == "EXPORT"):
            self.export_table(command[1], command[2])
        elif(cmd == "RENAME"):
            self.rename_table(command[1], command[2])
        elif(cmd == "PRINT"):
            self.print_table(command[1])
        elif(cmd == "DISCARD"):
            self.discard_table(command[1])
    
    def import_table(self, table_name, filename):
        data = self.filesCSV.read_csv(self.filePath + filename)
        if(data):
            self.tablesData[table_name] = data
           
    def export_table(self, table_name, filename):
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return
        self.filesCSV.write_csv(filename, self.tablesData[table_name])

    def rename_table(self, table_name, new_name):
        if table_name in self.tablesData:
            self.tablesData[new_name] = self.tablesData.pop(table_name)
            print(f"Table {table_name} renamed to {new_name}.")
        else:
            print(f"Table {table_name} does not exist.")

    def print_table(self, table_name):
        if table_name in self.tablesData:
            data = self.tablesData[table_name]
            print(data)
        else:
            print(f"Table {table_name} does not exist.")

    def discard_table(self, table_name):
        if table_name in self.tablesData:
            self.tablesData.pop(table_name)
        else:
            print(f"Table {table_name} not found.")    
