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
            | export_command"""
        p[0] = p[1]

    def p_import_command(self, p):
        """import_command : IMPORT TABLE ID FROM STRING ';'"""
        print(f"Importing table {p[3]} from file {p[5]}")
        p[0] = ("IMPORT", p[3], p[5])

    def p_export_command(self, p):
        """export_command : EXPORT TABLE ID AS STRING ';'"""
        print(f"Exporting table {p[3]} from file {p[5]}")
        p[0] = ("EXPORT", p[3], p[5])

    def p_error(self, p):
        if p:
            print(f"Syntax error at {p.value!r}")
        else:
            print("Syntax error at EOF")

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)
