import ply.yacc as yacc
from lexer import Lexer

class Parser:
    def __init__(self):
        self.lexer = Lexer()
        self.lexer.build()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)

    def p_program(self, p):
        """program : table_command 
                   | program table_command"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_table_command(self, p):
        """table_command : import_command
            | export_command
            | rename_command
            | print_command
            | discard_command"""
        p[0] = p[1]

    def p_import_command(self, p):
        """import_command : IMPORT TABLE ID FROM STRING SEMICOLON"""
        print(f"Importing table {p[3]} from file {p[5]}")
        p[0] = ("IMPORT", p[3], p[5])

    def p_export_command(self, p):
        """export_command : EXPORT TABLE ID AS STRING SEMICOLON"""
        print(f"Exporting table {p[3]} from file {p[5]}")
        p[0] = ("EXPORT", p[3], p[5])
    
    def p_discard_command(self, p):
        """discard_command : DISCARD TABLE ID SEMICOLON"""
        print(f"Discarding table {p[3]} from program memory")
        p[0] = ("DISCARD", p[3])

    def p_rename_commmand(self, p):
        """rename_command : RENAME TABLE ID STRING SEMICOLON"""
        print(f"Renaming {p[3]} to {p[4]}")
        p[0] = ("RENAME", p[3], p[4])

    def p_print_command(self, p):
        """print_command : PRINT TABLE ID SEMICOLON"""
        print(f"Printing table {p[3]}")
        p[0] = ("PRINT", p[3])

    def p_error(self, p):
        if p:
            print(f"Syntax error at {p.value!r}")
        else:
            print("Syntax error at EOF")

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)
