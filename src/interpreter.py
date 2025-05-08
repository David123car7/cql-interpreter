import csv
from parser import Parser
from filesCSV import FilesCSV

class Interpreter:
    """
    The Interpreter class runs parsed commands and manages in-memory tables read from CSV files.
    Attributes:
        parser (Parser): The YACC parser for interpreting CQL commands.
        filesCSV (FilesCSV): Utility for reading and writing CSV files.
        tablesData (dict): In-memory storage of tables keyed by table name.
        filePath (str): Default directory path for CSV files.
    """
    def __init__(self):
        """
        Initialize the Interpreter with a Parser, FilesCSV utility,
        and empty tablesData storage.
        """
        self.parser = Parser()
        self.filesCSV = FilesCSV()
        self.tablesData = {}
        self.filePath = "files/"
        self.procedures = {}

    def run(self, data):
        """
        Parse and execute a block of CQL commands.
        Args:
            data (str): The raw CQL commands string to run.
        Returns:
            None
        """
        result = self.parser.parse(data)
        if result is None:
            print("No result from parser")
            return None
        for cmd in result:
            self.execute(cmd)

    def execute(self, command):
        """
        Dispatch and execute a single parsed command tuple.
        Args:
            command (tuple): Parsed command in the form (CMD_TYPE, ...).
        Returns:
            None
        """
        cmd = command[0]
        if cmd == "IMPORT":
            self.import_table(command[1], command[2])
        elif cmd == "EXPORT":
            self.export_table(command[1], command[2])
        elif cmd == "RENAME":
            self.rename_table(command[1], command[2])
        elif cmd == "PRINT":
            self.print_table(command[1])
        elif cmd == "DISCARD":
            self.discard_table(command[1])
        elif cmd == "SELECT_NO_LIMIT":
            self.select_table(command[1])
        elif cmd == "SELECT_LIMIT":
            self.select_table(command[1], command[2])
        elif cmd == "SELECT_SPECIFIC_NO_LIMIT":
            self.select_specific(command[2], command[1])
        elif cmd == "SELECT_SPECIFIC_LIMIT":
            self.select_specific(command[2], command[1], command[3])
        elif cmd == "SELECT_WHERE_NO_LIMIT":
            self.select_where(command[1], command[2])
        elif cmd == "SELECT_WHERE_LIMIT":
            self.select_where(command[1], command[2], command[3])
        elif cmd == "CREATE_TABLE_SELECT_NO_LIMIT":
            self.create_table_select(command[1], command[2])
        elif cmd == "CREATE_TABLE_SELECT_LIMIT":
            self.create_table_select(command[1], command[2], command[3])
        elif cmd == "CREATE_TABLE_SELECT_WHERE_NO_LIMIT":
            self.create_table_select_where(command[1],command[2], command[3])
        elif cmd == "CREATE_TABLE_SELECT_WHERE_LIMIT":
            self.create_table_select_where(command[1], command[2], command[3], command[4])
        elif cmd == "PROCEDURE":
            self.procedure(command[1], command[2])
        elif cmd == "CREATE_TABLE_FROM_JOIN":
            self.create_table_from_join(command[1], command[2], command[3], command[4])

    def import_table(self, table_name, filename):
        """
        Import a CSV file into memory as a table.
        Args:
            table_name (str): Name to assign to the imported table.
            filename (str): CSV filename to read (relative to filePath).
        Returns:
            None
        """
        data = self.filesCSV.read_csv(self.filePath + filename)
        if data:
            self.tablesData[table_name] = data

    def export_table(self, table_name, filename):
        """
        Export an in-memory table to a CSV file.
        Args:
            table_name (str): Name of the table to export.
            filename (str): Destination CSV filename.
        Returns:
            None
        """
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return
        self.filesCSV.write_csv(filename, self.tablesData[table_name])

    def rename_table(self, table_name, new_name):
        """
        Rename a table stored in memory.
        Args:
            table_name (str): Current name of the table.
            new_name (str): New name for the table.
        Returns:
            None
        """
        if table_name in self.tablesData:
            self.tablesData[new_name] = self.tablesData.pop(table_name)
            print(f"Table {table_name} renamed to {new_name}.")
        else:
            print(f"Table {table_name} does not exist.")

    def print_table(self, table_name):
        """
        Print an in-memory table's contents.
        Args:
            table_name (str): Name of the table to print.
        Returns:
            None
        """
        if table_name in self.tablesData:
            data = self.tablesData[table_name]
            print(data)
        else:
            print(f"Table {table_name} does not exist.")

    def discard_table(self, table_name):
        """
        Remove a table from memory.
        Args:
            table_name (str): Name of the table to discard.
        Returns:
            None
        """
        if table_name in self.tablesData:
            self.tablesData.pop(table_name)
        else:
            print(f"Table {table_name} not found.")

    def select_table(self, table_name, limit=None):
        """
        Print all rows (up to optional limit) of a table.
        Args:
            table_name (str): Name of the table to select from.
            limit (int, optional): Maximum number of rows to display.
        Returns:
            dict: A dictionary with keys 'header' (list of column names) and
                'data' (list of rows), or None if invalid.
        """
        if not table_name:
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None

        selectedTable = []
        data = self.tablesData[table_name]
        dataLimit = int(limit) if limit is not None else None
        header = data.get("header")
        rows = data.get("data")
        for row in rows[:dataLimit]:
            selectedTable.append(row)
        
        print(header)
        print(selectedTable)
        return {"header": header, "data": selectedTable}


    def select_specific(self, table_name, columns, limit=None):
        """
        Return selected rows from a table based on one or more numerical conditions.

        Args:
            table_name (str): Name of the table to query.
            condition (list of tuples): Each tuple describes a filter in the form
                (column_name, operator, value)
            limit (int, optional): Maximum number of rows to scan from the table.

        Returns:
            dict: A dictionary with keys 'header' (list of column names) and
                'data' (list of rows matching all conditions), or None if invalid.
        """
        if not table_name:
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None

        data = self.tablesData[table_name]
        header = data.get("header")
        rows = data.get("data")

        for col in columns:
            if col not in header:
                print(f"Column {col} does not exist in table {table_name}.")
                return None

        selectedTable = []
        column_indices = [header.index(col) for col in columns]
        dataLimit = int(limit) if limit is not None else None
        for row in rows[:dataLimit]:
            selected_row = [row[i] for i in column_indices]
            selectedTable.append(selected_row)
        
        print(columns)
        print(selectedTable)
        return {"header": columns, "data": selectedTable}


    def select_where(self, table_name, condition, limit=None):
        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None
        
        data = self.tablesData.get(table_name)
        dataLimit = int(limit) if limit is not None else None
        intermediate = {}

        index = 0
        header = data.get("header")
        rows = data.get("data")
        for c in condition: 
            filtered = []
            for row in rows[:dataLimit]:
                cell = row[header.index(c[1])]
                cond = c[2]
                value = c[3]
                if cond == "=" and float(cell) == value:
                    filtered.append(row)
                elif cond == "!=" and float(cell) != value:
                    filtered.append(row)
                elif cond == "<" and float(cell) < value:
                    filtered.append(row)
                elif cond == ">" and float(cell) > value:
                    filtered.append(row)
                elif cond == "<=" and float(cell) <= value:
                    filtered.append(row)
                elif cond == ">=" and float(cell) >= value:
                    filtered.append(row)
            intermediate[index] = filtered
            index += 1
  
        parsed_data = []
        index = 0
        dictLenght = len(intermediate)
        if(dictLenght != 1):
            for i in intermediate:
                for j in intermediate[i]:
                    if(i+1 > dictLenght):
                        break
                    for k in intermediate[i+1]:
                        if(j[0] == k[0]):
                            parsed_data.append(k)
                break
        else:
            parsed_data = intermediate[0]
        
        print(header)
        print(parsed_data)
        return {"header": header, "data": parsed_data}
    
    def create_table_select(self, new_table, table_name, limit=None):
        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None
        if new_table in self.tablesData:
            print(f"Table {new_table} already exists.")
            return None
        
        self.tablesData[new_table]= self.select_table(table_name, limit)
        print(f"Table {new_table} created from {table_name}.")
        return True
    
    def create_table_select_where(self, new_table, table_name, condition, limit=None):
        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None
        if new_table in self.tablesData:
            print(f"Table {new_table} already exists.")
            return None
        
        self.tablesData[new_table] = self.select_where(table_name, condition, limit)
        print(f"Table {new_table} created from {table_name} with condition {condition}")

    def procedure(self, name, command):
        """
        Create a procedure with the given name and command.
        Args:
            name (str): Name of the procedure.
            command (str): Command to execute when the procedure is called.
        Returns:
            None
        """
        if name in self.tablesData:
            print(f"Procedure {name} already exists.")
            return False
        
        if command == "":
            print("Command is empty")
            return False

        for cmd in command:
            self.execute(cmd)
    
    def create_table_from_join(self, new_table, table_name1, table_name2, id):
        if table_name1 == "":
            print("Table name is empty")
            return None
        if table_name1 not in self.tablesData:
            print(f"Table {table_name1} does not exist.")
            return None
        if table_name2 == "":
            print("Table name is empty")
            return None
        if table_name2 not in self.tablesData:
            print(f"Table {table_name2} does not exist.")
            return None
        if new_table in self.tablesData:
            print(f"Table {new_table} already exists.")
            return None
        
        data1 = self.tablesData[table_name1]
        data2 = self.tablesData[table_name2]
        header1 = data1.get("header")
        header2 = data2.get("header")

        if id not in header1 or id not in header2:
            print(f"Column {id} does not exist in one of the tables.")
            return None
        
        index1 = header1.index(id)
        index2 = header2.index(id)
        new_header = header1 + [col for col in header2 if col != id]
        new_tableData = []
        for row1 in data1["data"]:
            join_val = row1[index1]
            for row2 in data2["data"]:
                if row2[index2] == join_val:
                    new_row = row1 + [
                        row2[i] for i in range(len(row2)) if data2["header"][i] != id
                    ]
                    print(new_row)
                    new_tableData.append(new_row)
        
        # Store result
        self.tablesData[new_table] = {"header": new_header, "data": new_tableData}
        


