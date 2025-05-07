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
        elif(cmd == "SELECT_NO_LIMIT"):
            self.select_table(command[1])
        elif(cmd == "SELECT_LIMIT"):
            self.select_table_Limit(command[1], command[2])
        elif(cmd == "SELECT_SPECIFIC_NO_LIMIT"):
            self.select_specific(command[2], command[1])
        elif(cmd == "SELECT_SPECIFIC_LIMIT"):
            self.select_specific_Limit(command[2], command[1], command[3])
        elif(cmd == "SELECT_WHERE"):
            self.select_where(command[1], command[2])
            
    
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

    # Select a table from the imported tables
    # This function is used to select a table from the imported tables.
    def select_table(self, table_name):
        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None
        data = self.tablesData.get(table_name)

        header = data.get("header", [])
        rows = data.get("data", [])

        print("Table:", table_name)
        print(header)
        for row in rows:
            print(row)
        return data
    
    # Select specific columns from a table
    # This function is used to select specific columns from a table.
    def select_specific(self, table_name,columns):
        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None         
        data = self.tablesData.get(table_name)
        header = data.get("header")
        rows = data.get("data")

        for column in columns:
            if column not in header:
                print(f"Column {column} does not exist in table {table_name}.")
                return None

        # Get the indices of the columns to select
        column_indices = [header.index(col) for col in columns]
  
        print(columns)

        for row in rows:
            selected_row = [row[i] for i in column_indices]
            print(selected_row)

    #Select a limited number of rows from a table
    # This function is used to select a limited number of rows from a table.    
    def select_table_Limit(self, table_name,limit):

        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None
        data = self.tablesData.get(table_name)

        header = data.get("header", [])
        rows = data.get("data", [])

        print(header)
        for row in rows[:limit]:
            print(row)
        return data
    
    def select_specific_Limit(self, table_name,columns,limit):
        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None         
        

        data = self.tablesData.get(table_name)
        header = data.get("header")
        rows = data.get("data")

        for column in columns:
            if column not in header:
                print(f"Column {column} does not exist in table {table_name}.")
                return None

        # Get the indices of the columns to select
        column_indices = [header.index(col) for col in columns]
  
        print(columns)

        for row in rows[:limit]:
            selected_row = [row[i] for i in column_indices]
            print(selected_row)

    #NAO FUNCIONA
    def select_where(self, table_name, condition):
        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None
        data = self.tablesData.get(table_name)
        

        header = data.get("header", [])
        rows = data.get("data", [])
        new_data= []
        print(header)
        for row in rows:
            for item in row:
                if condition in item:
                    new_data.append(row)
        print(new_data)
            
        return data