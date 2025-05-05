import ply.lex as plex

class Lexer:
    tokens = {'ID', 'STRING', 'IMPORT', 'TABLE', 'FROM'}
    literals = {',', '/', '-', '.', '[', ']', '"'}

    def build(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)
        return self.lexer #do i need to return this?




