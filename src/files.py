import csv


def split_line(line: str) -> list[str]:

    parts = []
    current_part = ""
    inside_brackets = False
    inside_quotes = False

    for char in line:
        if char == '"':
           inside_quotes = True
        if char == '[':
            inside_brackets = True
        elif char == ']':
            inside_brackets = False
        
        if char == ',' and not inside_brackets and not inside_quotes:
            parts.append(current_part.strip())
            current_part = ''
        else:
            current_part += char

    parts.append(current_part.strip())
    return parts

def load_file(filename: str) -> list[dict[str, str]]:
    """
    Lê um ficheiro CSV ignorando linhas comentadas e tratando aspas.
    Retorna uma lista de dicionários (coluna: valor).
    """
    dados = []

    with open(filename, 'r', newline='', encoding='utf-8') as file:
        # Filtra linhas que não são comentários
        lines = [linha for linha in file if not linha.strip().startswith("#")]

        if not lines:
            return []

        line_bracket = split_line(lines[0])

        for line in lines[1:]:
            values = split_line(line)
            row = dict(zip(line_bracket, values))
            dados.append(row)

    return dados
