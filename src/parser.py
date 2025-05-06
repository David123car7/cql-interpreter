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
                   | program table_command
                   | query_command
                   | program query_command"""
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

    def p_query_command(self, p):
        """query_command : selectAll_command
            | select_specific
            | select_where_command"""
        p[0] = p[1]
    
    #Table commands
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

    #Query commands
    def p_selectAll_command(self, p):
        """selectAll_command : SELECT ASTERISK FROM ID SEMICOLON"""
        print(f"Selecting all data from table {p[4]}")
        p[0] = ("SELECT", p[4])
    
    def p_select_specific(self, p):
        "select_specific : SELECT select_list FROM ID SEMICOLON"
        print(f"Selecting {p[2]} from table {p[4]}")
        p[0] = ("SELECT_SPECIFIC", p[2], p[4])
    
    def p_select_where_command(self, p):
        """select_where_command : SELECT select_list FROM ID WHERE condition SEMICOLON"""
        p[0] = ("SELECT_WHERE", p[2], p[4], p[6])

    def p_condition(self, p):
        """condition : ID EQUALS value
        | ID NOT_EQUALS value
        | ID LESS_THAN value
        | ID GREATER_THAN value
        | ID LESS_EQUALS value
        | ID GREATER_EQUALS value
        | condition AND condition"""
        if len(p) == 4 and p[2] != "AND":
            p[0] = ("CONDITION", p[1], p[2], p[3])
        elif len(p) == 4 and p[2] == "AND":
            p[0] = ("AND", p[1], p[3])

    def p_value(self, p):
        """value : ID
        | STRING
        | NUMBER"""
        p[0] = p[1]
    
    def p_select_list_multi(self, p):
        "select_list : select_list COMMA ID"
        p[0] = p[1] + [p[3]]

    def p_select_list_single(self, p):
        "select_list : ID"
        p[0] = [p[1]]

    def p_error(self, p):
        if p:
            print(f"Syntax error at {p.value!r}")
        else:
            print("Syntax error at EOF")

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)
