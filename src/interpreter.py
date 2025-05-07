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
            None
        """
        if not table_name:
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None

        data = self.tablesData[table_name]
        dataLimit = int(limit) if limit is not None else None
        header = data.get("header", [])
        rows = data.get("data", [])
        print(header)
        for row in rows[:dataLimit]:
            print(row)

    def select_specific(self, table_name, columns, limit=None):
        """
        Print specific columns (up to optional limit) of a table.
        Args:
            table_name (str): Name of the table to select from.
            columns (list of str): Column names to display.
            limit (int, optional): Maximum number of rows to display.
        Returns:
            None
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

        column_indices = [header.index(col) for col in columns]
        dataLimit = int(limit) if limit is not None else None

        print(columns)
        for row in rows[:dataLimit]:
            selected_row = [row[i] for i in column_indices]
            print(selected_row)

    def select_where(self, table_name, condition, limit=None):
        """
        Print rows satisfying a WHERE condition, with optional limit.
        Args:
            table_name (str): Name of the table to query.
            condition (tuple): A condition tuple, e.g., ("CONDITION", col, op, val).
            limit (int, optional): Maximum number of rows to display.
        Returns:
            dict or None: Filtered table with "header" and "data" keys, or None.
        """
        if table_name == "":
            print("Table name is empty")
            return None
        if table_name not in self.tablesData:
            print(f"Table {table_name} does not exist.")
            return None
        
        data = self.tablesData.get(table_name)
        dataLimit = int(limit) if limit is not None else None
        id = condition[1] 
        value = condition[3]
        condition = condition[2]
        new_data = []

        header = data.get("header")
        rows = data.get("data")
        for row in rows[:dataLimit]:
            cell = row[header.index(id) ]
            if condition == "=" and float(cell) == value:
                new_data.append(row)
            elif condition == "!=" and float(cell) != value:
                new_data.append(row)
            elif condition == "<" and float(cell) < value:
                new_data.append(row)
            elif condition == ">" and float(cell) > value:
                new_data.append(row)
            elif condition == "<=" and float(cell) <= value:
                new_data.append(row)
            elif condition == ">=" and float(cell) >= value:
                new_data.append(row)

        print(header)
        print(new_data)