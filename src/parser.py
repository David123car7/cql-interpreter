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
        p[0] = ("IMPORT", p[3], p[5])

    def p_export_command(self, p):
        """export_command : EXPORT TABLE ID AS STRING SEMICOLON"""
        p[0] = ("EXPORT", p[3], p[5])
    
    def p_discard_command(self, p):
        """discard_command : DISCARD TABLE ID SEMICOLON"""
        p[0] = ("DISCARD", p[3])

    def p_rename_commmand(self, p):
        """rename_command : RENAME TABLE ID STRING SEMICOLON"""
        print(f"Renaming {p[3]} to {p[4]}")
        p[0] = ("RENAME", p[3], p[4])

    def p_print_command(self, p):
        """print_command : PRINT TABLE ID SEMICOLON"""
        p[0] = ("PRINT", p[3])

    #Query commands
    
    def p_selectAll_command(self, p):
        """selectAll_command : selectAll_command_no_limit
        | selectAll_command_limit"""
        p[0] = p[1]

    def p_selectAll_command_no_limit(self, p):
        """selectAll_command_no_limit : SELECT ASTERISK FROM ID SEMICOLON"""
        p[0] = ("SELECT_NO_LIMIT", p[4])

    
    def p_selectAll_command_limit(self, p):
        """selectAll_command_limit : SELECT ASTERISK FROM ID LIMIT NUMBER SEMICOLON"""
        p[0] = ("SELECT_LIMIT", p[4], p[6])
    
    
    def p_select_specific(self, p):
        """select_specific : select_specific_no_limit
        | select_specific_limit"""
        p[0] = p[1]

    def p_select_specific_no_limit(self, p):
        """select_specific_no_limit : SELECT select_list FROM ID SEMICOLON"""
        p[0] = ("SELECT_SPECIFIC_NO_LIMIT", p[2], p[4])

    def p_select_specific_limit(self, p):
        """select_specific_limit : SELECT select_list FROM ID LIMIT NUMBER SEMICOLON"""
        p[0] = ("SELECT_SPECIFIC_LIMIT", p[2], p[4], p[6])
    
    def p_select_where_command(self, p):
        """select_where_command : select_where_command_no_limit
        | select_where_command_limit"""
        p[0] = p[1]
        
    #MISSING 
    def p_select_where_command_no_limit(self, p):
        """select_where_command_no_limit : SELECT ASTERISK FROM ID WHERE condition SEMICOLON"""
        p[0] = ("SELECT_WHERE_NO_LIMIT", p[4], p[6])
    #MISSING
    def p_select_where_command_limit(self, p):
        """select_where_command_limit : SELECT ASTERISK FROM ID WHERE condition LIMIT NUMBER SEMICOLON"""
        p[0] = ("SELECT_WHERE_LIMIT", p[4], p[6], p[8])

    def p_condition(self, p):
        """condition : ID EQUALS NUMBER
        | ID NOT_EQUALS NUMBER
        | ID LESS_THAN NUMBER
        | ID GREATER_THAN NUMBER
        | ID LESS_EQUALS NUMBER
        | ID GREATER_EQUALS NUMBER
        | condition AND condition"""
        if len(p) == 4 and p[2] != "AND":
            p[0] = ("CONDITION", p[1], p[2], p[3])
        elif len(p) == 4 and p[2] == "AND":
            p[0] = ("AND", p[1], p[3])
    
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
