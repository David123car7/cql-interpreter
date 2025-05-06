import ply.lex as plex

class Lexer:
    tokens  = ['ID', 'STRING', 'IMPORT', 'EXPORT','TABLE', 'FROM', 'AS']
    literals = [',', ';']
    t_ignore = ' \t\n'

    def build(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)
        return self.lexer
    
    def input(self, data):
        self.lexer.input(data)

    def t_IMPORT(self, t):
        r'IMPORT'
        return t
    
    def t_EXPORT(self, t):
        r'EXPORT'
        return t
    
    def t_AS(self, t):
        r'AS'
        return t
    
    def t_TABLE(self, t):
        r'TABLE'
        return t
    
    def t_FROM(self, t):
        r'FROM'
        return t 

    def t_ID(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        return t

    def t_STRING(self, t):
        r'\"([^\\\"]|\\.)*\"'
        t.value = t.value[1:-1]
        return t

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
