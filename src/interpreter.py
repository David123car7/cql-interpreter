import csv


def load_observacoes(filename: str) -> list[list[str]]:
    """
    Lê todo o CSV e devolve uma lista de listas (cada sub-lista é uma linha).
    """
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)


